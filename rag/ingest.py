import logging
import re
from pathlib import Path

import fitz

from .config import CHUNK_OVERLAP, CHUNK_SIZE, DATA_DIR, SCHEME_NAMES

log = logging.getLogger(__name__)


def clean_page(text: str) -> str:
    text = re.sub(r"(?<=[A-Za-z])-[ \t]*\n[ \t]*(?=[a-z])", "", text)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    counts = {}
    for line in lines:
        counts[line] = counts.get(line, 0) + 1
    lines = [line for line in lines if counts[line] < 3]
    return re.sub(r"\s+", " ", "\n\n".join(lines)).strip()


def split_page(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    # Keep numbered clauses and paragraph boundaries where possible.
    sections = re.split(r"(?=\b\d+(?:\.\d+)+\b)|\n\s*\n", text)
    chunks, current = [], ""
    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(current) + len(section) + 1 <= size:
            current = f"{current}\n\n{section}".strip()
            continue
        if current:
            chunks.append(current)
        if len(section) > size:
            start = 0
            while start < len(section):
                end = min(len(section), start + size)
                if end < len(section):
                    boundary = section.rfind(" ", start, end)
                    if boundary > start + size * 0.65:
                        end = boundary
                chunks.append(section[start:end].strip())
                if end == len(section):
                    break
                start = max(start + 1, end - overlap)
            current = ""
        else:
            current = section
    if current:
        chunks.append(current)
    return chunks


def load_pages(data_dir: Path = DATA_DIR):
    pages = []
    for pdf_path in sorted(data_dir.glob("*.pdf")):
        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(doc, 1):
            text = clean_page(page.get_text("text"))
            if len(text) < 100:
                log.warning("Skipping short or scanned page: %s page %d (%d chars)", pdf_path.name, page_num, len(text))
                continue
            pages.append({"source_file": pdf_path.name, "scheme": SCHEME_NAMES.get(pdf_path.name, pdf_path.stem), "page": page_num, "text": text})
    return pages


def make_chunks(data_dir: Path = DATA_DIR):
    out = []
    for page in load_pages(data_dir):
        for text in split_page(page["text"]):
            out.append({**{k: page[k] for k in ("source_file", "scheme", "page")}, "chunk_id": len(out), "text": text})
    return out
