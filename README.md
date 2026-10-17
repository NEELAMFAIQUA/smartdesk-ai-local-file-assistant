# Local File Assistant

An original, retrieval-only text-document demo. Select `.txt` files explicitly,
ask a question, and inspect relevant excerpts with file and chunk citations.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Only selected text files are read, in memory for the current app session. This
prototype makes no model or network calls and does not write uploaded content to
disk. PDFs are not supported in this minimal version.

Run tests with `python -m unittest discover -s tests -v`.
