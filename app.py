import streamlit as st

from documents import answer_with_local_ollama, chunk_text, read_uploaded_file, retrieve

st.set_page_config(page_title="Local Text Assistant", page_icon="📄")
st.title("Local PDF & Text Assistant")
st.caption("Ask questions over explicitly selected PDF and text files.")
files = st.file_uploader(
    "Select PDF or text files",
    type=["pdf", "txt"],
    accept_multiple_files=True,
    help="Files are used in memory for this session and are not uploaded to a model.",
)

chunks = []
for file in files or []:
    try:
        text = read_uploaded_file(file.name, file.getvalue())
    except (ValueError, UnicodeError, OSError) as error:
        st.error(f"Could not read {file.name}: {error}")
        continue
    chunks.extend(chunk_text(text, file.name))

if not chunks:
    st.info("Select one or more PDF or text files to begin.")
else:
    st.success(f"Read selected files into {len(chunks)} in-memory text chunks.")
    mode = st.radio(
        "Answer mode",
        ["Local retrieval only", "Generate with local Ollama"],
        horizontal=True,
    )
    model = ""
    if mode == "Generate with local Ollama":
        model = st.text_input("Installed Ollama model name", value="llama3.2")
        st.caption("Generation calls Ollama at localhost only; install and start Ollama first.")
    question = st.text_input("Search your selected files")
    if question:
        results = retrieve(question, chunks)
        if not results:
            st.warning("No matching excerpts found.")
        elif mode == "Generate with local Ollama" and st.button("Ask local model"):
            try:
                response, results = answer_with_local_ollama(
                    question, chunks, model
                )
                st.markdown(response)
            except (OSError, RuntimeError) as error:
                st.error(f"Local Ollama request failed: {error}")
        for result in results:
            st.markdown(
                f"**{result['source']} — chunk {result['chunk']}** "
                f"(match score {result['score']})"
            )
            st.write(result["text"])
st.caption("Selected documents are processed in memory. No remote model is used.")
