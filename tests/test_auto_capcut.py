import tempfile
import unittest
from pathlib import Path

from auto_capcut import main, split_text


class SplitTextTests(unittest.TestCase):
    def test_prefers_sentence_boundaries(self):
        self.assertEqual(split_text("Câu một. Câu hai! Câu ba?", 18), ["Câu một. Câu hai!", "Câu ba?"])

    def test_normalizes_whitespace(self):
        self.assertEqual(split_text("  Một\n\n  hai   ba. ", 50), ["Một hai ba."])

    def test_long_sentence_is_split_on_words(self):
        blocks = split_text("một hai ba bốn năm sáu", 9)
        self.assertEqual(" ".join(blocks), "một hai ba bốn năm sáu")
        self.assertTrue(all(0 < len(block) <= 9 for block in blocks))

    def test_long_word_is_hard_split(self):
        self.assertEqual(split_text("abcdefgh", 3), ["abc", "def", "gh"])

    def test_rejects_invalid_limit(self):
        with self.assertRaises(ValueError):
            split_text("text", 0)

    def test_empty_text(self):
        self.assertEqual(split_text(" \n "), [])


class CliTests(unittest.TestCase):
    def test_dry_run(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "story.txt")
            path.write_text("Xin chào. Đây là truyện.", encoding="utf-8")
            self.assertEqual(main([str(path), "--dry-run"]), 0)

    def test_missing_file(self):
        self.assertEqual(main(["missing-story.txt", "--dry-run"]), 2)


if __name__ == "__main__":
    unittest.main()
