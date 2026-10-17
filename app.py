import streamlit as st

from documents import chunk_text, retrieve

st.set_page_config(page_title="Local Text Assistant", page_icon="📄")
st.title("Local Text Assistant")
st.caption("Search selected text files with local, retrieval-only matching.")
files = st.file_uploader(
    "Select text files",
    type=["txt"],
    accept_multiple_files=True,
    help="Files are used in memory for this session and are not uploaded to a model.",
)

chunks = []
for file in files or []:
    text = file.getvalue().decode("utf-8", errors="replace")
    chunks.extend(chunk_text(text, file.name))

if not chunks:
    st.info("Select one or more .txt files to begin.")
else:
    st.success(f"Indexed {len(files)} selected file(s) as {len(chunks)} text chunks.")
    question = st.text_input("Search your selected files")
    if question:
        results = retrieve(question, chunks)
        if not results:
            st.warning("No matching excerpts found.")
        for result in results:
            st.markdown(
                f"**{result['source']} — chunk {result['chunk']}** "
                f"(match score {result['score']})"
            )
            st.write(result["text"])
st.caption("No generative answer or model call is used in this version.")
