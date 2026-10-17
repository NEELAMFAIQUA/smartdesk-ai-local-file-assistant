import unittest

from documents import chunk_text, retrieve


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


if __name__ == "__main__":
    unittest.main()
