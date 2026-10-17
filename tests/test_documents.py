import unittest
from io import BytesIO

from documents import chunk_text, read_uploaded_file, retrieve
from pypdf import PdfWriter


class DocumentTests(unittest.TestCase):
    def test_chunks_keep_source_and_sequential_numbers(self):
        chunks = chunk_text("one two three four five", "notes.txt", 2)
        self.assertEqual([chunk["chunk"] for chunk in chunks], [1, 2, 3])
        self.assertEqual(chunks[1]["source"], "notes.txt")

    def test_query_returns_best_matching_citation(self):
        chunks = chunk_text("apples and pears. Power bill uses kilowatt hours.", "home.txt", 4)
        results = retrieve("kilowatt hours", chunks)
        self.assertEqual(results[0]["source"], "home.txt")
        self.assertGreater(results[0]["score"], 0)

    def test_blank_query_has_no_results(self):
        self.assertEqual(retrieve(" ", []), [])

    def test_invalid_chunk_size_raises(self):
        with self.assertRaises(ValueError):
            chunk_text("sample", "sample.txt", 0)

    def test_txt_upload_is_decoded(self):
        self.assertEqual(
            read_uploaded_file("notes.txt", "hello local".encode("utf-8")),
            "hello local",
        )

    def test_pdf_upload_is_parsed_in_memory(self):
        pdf = BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        writer.write(pdf)
        self.assertEqual(read_uploaded_file("notes.pdf", pdf.getvalue()), "")

    def test_unsupported_upload_is_rejected(self):
        with self.assertRaises(ValueError):
            read_uploaded_file("notes.docx", b"contents")


if __name__ == "__main__":
    unittest.main()
