import os
import re

UNKNOWN = "I don't know based on the provided documents."


def llm_client():
    import streamlit as st
    key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    if key:
        from groq import Groq
        return Groq(api_key=key), os.getenv("LLM_MODEL", "openai/gpt-oss-120b")
    key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    if key:
        from google import genai
        return genai.Client(api_key=key), os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    return None, None


def rewrite_query(question, history, client, model):
    if not client:
        return question
    prompt = "Rewrite as a standalone, keyword-rich retrieval query. Resolve follow-ups from this conversation. Return only the query.\nHistory: " + str(history[-8:]) + "\nQuestion: " + question
    try:
        if hasattr(getattr(client, "models", None), "generate_content"):
            result = client.models.generate_content(model=model, contents=prompt, config={"temperature": 0})
            return result.text.strip()
        if hasattr(client, "chat"):
            result = client.chat.completions.create(model=model, temperature=0, messages=[{"role": "user", "content": prompt}])
            return result.choices[0].message.content.strip()
        return question
    except Exception:
        return question


def answer(question, chunks, client, model):
    print('DEBUG client:', type(client).__name__, '| model:', model, '| chunks:', len(chunks or []), flush=True)
    if not client or not chunks:
        print('DEBUG exit: no client or no chunks', flush=True)
        return UNKNOWN
    context = "\n\n".join(f"[{i}] ({c['scheme']}, {c['source_file']}, page {c['page']})\n{c['text']}" for i, c in enumerate(chunks, 1))
    system = "Answer ONLY from provided context. If absent, reply exactly: I don't know based on the provided documents. Do not use outside knowledge or guess amounts, dates or income limits. Cite every factual claim with plain square-bracket numbers like [1] or [2] matching the context numbers; never use any other citation format. Keep answers short and plain-language, then add a one-line summary. If sources conflict, describe the conflict and name both. Temperature 0."
    try:
        if hasattr(getattr(client, "models", None), "generate_content"):
            result = client.models.generate_content(model=model, contents=f"{system}\nQuestion: {question}\nContext:\n{context}", config={"temperature": 0})
            text = result.text.strip()
        elif hasattr(client, "chat"):
            result = client.chat.completions.create(model=model, temperature=0, messages=[{"role": "system", "content": system}, {"role": "user", "content": f"Question: {question}\n\nContext:\n{context}"}])
            text = result.choices[0].message.content.strip()
        else:
            return UNKNOWN
    except Exception as e:
        print('LLM ERROR:', repr(e), flush=True)
        return UNKNOWN
    print('DEBUG raw LLM text:', repr(text[:400]), flush=True)
    text = re.sub(r'\u3010\s*(\d+)[^\u3011]*\u3011', r'[\1]', text)
    refs = {int(n) for n in re.findall(r"\[(\d+)\]", text)}
    valid = {n for n in refs if 1 <= n <= len(chunks)}
    if not valid or UNKNOWN in text:
        return UNKNOWN
    return text, [chunks[n - 1] for n in sorted(valid)]
