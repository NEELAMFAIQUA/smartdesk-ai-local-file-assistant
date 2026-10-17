"""In-memory text splitting and retrieval for user-selected local files."""

import re

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
