import json
import re


def safe_json_loads(raw_text, default=None):
    """Parse JSON from Gemini-style responses that may include markdown fences or extra text."""
    if default is None:
        default = {}

    if not raw_text:
        return default

    text = raw_text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        text = match.group(0)

    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError, ValueError):
        try:
            return json.loads(text.replace("'", '"'))
        except (json.JSONDecodeError, TypeError, ValueError):
            return default
