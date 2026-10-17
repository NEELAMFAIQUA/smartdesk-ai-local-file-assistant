"""In-memory text splitting and retrieval for user-selected local files."""

import re
from io import BytesIO

_TOKEN = re.compile(r"[a-z0-9]+")


def chunk_text(text, source, words_per_chunk=120):
    if words_per_chunk < 1:
        raise ValueError("words_per_chunk must be positive")
    words = text.split()
    return [
        {
            "source": source,
            "chunk": index // words_per_chunk + 1,
            "text": " ".join(words[index:index + words_per_chunk]),
        }
        for index in range(0, len(words), words_per_chunk)
    ]


def retrieve(question, chunks, limit=3):
    if limit < 1:
        raise ValueError("limit must be positive")
    query_terms = set(_TOKEN.findall(question.lower()))
    if not query_terms:
        return []
    scored = []
    for index, chunk in enumerate(chunks):
        tokens = set(_TOKEN.findall(chunk["text"].lower()))
        overlap = len(query_terms & tokens)
        if overlap:
            scored.append((overlap, index, chunk))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [{**chunk, "score": score} for score, _, chunk in scored[:limit]]


def read_uploaded_file(filename, content):
    """Extract text from a selected TXT or PDF upload, in memory."""
    suffix = filename.lower().rsplit(".", 1)[-1]
    if suffix == "txt":
        return content.decode("utf-8", errors="replace")
    if suffix == "pdf":
        from pypdf import PdfReader

        reader = PdfReader(BytesIO(content))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raise ValueError("Only .txt and .pdf files are supported")


def answer_with_local_ollama(question, chunks, model, base_url="http://localhost:11434"):
    """Use a local Ollama server only; retrieved excerpts remain on this machine."""
    import requests

    references = retrieve(question, chunks, limit=4)
    if not references:
        return "I couldn't find an answer in the selected files.", references
    context = "\n\n".join(
        f"[{item['source']} · chunk {item['chunk']}]\n{item['text']}"
        for item in references
    )
    response = requests.post(
        f"{base_url.rstrip('/')}/api/generate",
        json={
            "model": model,
            "prompt": (
                "Answer the question using only the provided excerpts. "
                "If they do not answer it, say so. Cite the source filename.\n\n"
                f"Excerpts:\n{context}\n\nQuestion: {question}"
            ),
            "stream": False,
        },
        timeout=90,
    )
    response.raise_for_status()
    payload = response.json()
    answer = payload.get("response", "").strip()
    if not answer:
        raise RuntimeError("The local model returned an empty answer.")
    return answer, references
