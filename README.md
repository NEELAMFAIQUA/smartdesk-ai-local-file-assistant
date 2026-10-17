# Local File Assistant

An original local PDF/TXT assistant. Select documents explicitly, retrieve
relevant excerpts with source citations, and optionally ask an Ollama model
running on `localhost` to form a grounded answer.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Only selected files are read in memory for the current app session. Retrieval
works without a model. For generation, install and start Ollama locally and
download a model such as `llama3.2`; the app calls only the local Ollama API.
Uploaded content is not sent to a hosted service or written to disk.

Run tests with `python -m unittest discover -s tests -v`.
