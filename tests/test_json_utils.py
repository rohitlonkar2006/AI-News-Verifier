import unittest

from utils.json_utils import safe_json_loads


class JsonUtilsTests(unittest.TestCase):
    def test_parses_markdown_json_with_extra_text(self):
        raw = '''```json
{
  "title": "Sample title",
  "article": "Sample article body"
}
```
'''

        self.assertEqual(
            safe_json_loads(raw),
            {"title": "Sample title", "article": "Sample article body"},
        )

    def test_extracts_json_object_from_surrounding_text(self):
        raw = 'Here is the result: {"title": "Another title", "article": "Body text"} Thanks!'

        self.assertEqual(
            safe_json_loads(raw),
            {"title": "Another title", "article": "Body text"},
        )

    def test_returns_default_for_invalid_payload(self):
        raw = 'This is not valid json at all.'

        self.assertEqual(safe_json_loads(raw, default={"title": "", "article": ""}), {"title": "", "article": ""})


if __name__ == "__main__":
    unittest.main()
