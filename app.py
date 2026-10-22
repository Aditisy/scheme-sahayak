import html
import re

import streamlit as st

from rag.config import SCHEME_NAMES, SIM_THRESHOLD
from rag.generate import UNKNOWN, answer, llm_client, rewrite_query
from rag.index import load_index
from rag.retrieve import retrieve

st.set_page_config(page_title="Scheme Sahayak", page_icon="🏛️", layout="wide")
st.title("Scheme Sahayak")
st.caption("Ask official government scheme documents in plain language.")


def source_text(text, question):
    escaped = html.escape(text)
    terms = sorted({w for w in re.findall(r"[\w-]{4,}", question.lower())}, key=len, reverse=True)
    for term in terms:
        escaped = re.sub(re.escape(term), lambda m: f"<mark>{m.group(0)}</mark>", escaped, flags=re.IGNORECASE)
    return escaped


@st.cache_resource(show_spinner="Loading the document index and CPU model...")
def resources():
    return (*load_index(), *llm_client())


with st.sidebar:
    st.header("Explore")
    choices = ["All", "PM-KISAN", "PM-JAY", "Post-Matric Scholarship (SC)"]
    selected = st.selectbox("Scheme filter", choices)
    st.markdown("**Example questions**")
    examples = ["How much assistance does PM-KISAN provide?", "Who can receive PM-KISAN benefits?", "What does PM-JAY cover?", "Who is eligible for the SC post-matric scholarship?", "What documents are needed to apply?", "Who won the 2023 cricket world cup?"]
    for q in examples:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("**About / limitations**\n\nGuidelines are snapshots and may be amended. This tool is informational, not legal advice. Confirm current rules with the responsible department.")

if "messages" not in st.session_state:
    st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "found" in msg:
            color = "#198754" if msg["found"] else "#b7791f"
            label = "Answer found in documents" if msg["found"] else "Not in the documents"
            st.markdown(f"<span style='color:{color};font-weight:700'>{label} · retrieval confidence {msg['confidence']:.2f}</span>", unsafe_allow_html=True)
            if msg.get("sources"):
                with st.expander("Sources"):
                    for c in msg["sources"]:
                        st.markdown(f"**{c['scheme']}** · `{c['source_file']}` · page {c['page']}\n\n{source_text(c['text'], msg.get('question', ''))}", unsafe_allow_html=True)

question = st.chat_input("Ask about eligibility, benefits, or documents")
if not question and st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            chunks, dense, bm25, model, client, llm_model = resources()
            history = [(m["role"], m["content"]) for m in st.session_state.messages[-8:-1]]
            rewritten = rewrite_query(question, history, client, llm_model)
            found_chunks, confidence, refused = retrieve(rewritten, chunks, dense, bm25, model, None if selected == "All" else selected)
            result = UNKNOWN if refused else answer(question, found_chunks, client, llm_model)
            if isinstance(result, tuple):
                response, sources = result
                found = True
            else:
                response, sources, found = result, [], False
            st.markdown(response)
            color = "#198754" if found else "#b7791f"
            label = "Answer found in documents" if found else "Not in the documents"
            st.markdown(f"<span style='color:{color};font-weight:700'>{label} · retrieval confidence {confidence:.2f}</span>", unsafe_allow_html=True)
            if sources:
                with st.expander("Sources", expanded=True):
                    for c in sources:
                        st.markdown(f"**{c['scheme']}** · `{c['source_file']}` · page {c['page']}\n\n{source_text(c['text'], question)}", unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": response, "found": found, "confidence": confidence, "sources": sources, "question": question})
        except Exception:
            st.warning("The document index or language model is unavailable. Please try again after setup is complete."); st.code(__import__("traceback").format_exc())


