import json
from utils.config import gemini
from utils.json_utils import safe_json_loads

def generate_explanation(title, article, prediction, confidence):
    prompt = f"""
        You are an expert journalist, linguistic fact-checking researcher, and Explainable AI (XAI) engine.
        A BiLSTM deep learning model has already processed this content body.

        Prediction Output Class: {prediction}
        Model Confidence Metric: {confidence:.2f}%

        Target News Title: {title}
        Target News Article Content: {article}

        Your tasks:
        1. Provide a clear summary evaluation under "summary".
        2. Supply clear verification factors into the "reasons" array list.
        3. Extract exactly 4 to 8 highly indicative words pushing towards credibility (if REAL) or deception indicators (if FAKE) and output them inside "supporting_words".
        4. Extract exactly 4 to 8 cross-examining words matching the opposite scale inside "opposing_words".
        5. Populate "highlight_phrases" with exact sentences/phrases from the article text that carry strong logical weight.

        Return ONLY a valid JSON string object matching this precise structural profile schema layout:
        {{
            "summary": "Executive summary sentence text...",
            "reasons": [
                "Linguistic factor reason 1...",
                "Linguistic factor reason 2..."
            ],
            "supporting_words": ["word1", "word2", "word3"],
            "opposing_words": ["word1", "word2", "word3"],
            "highlight_phrases": [
                "Exact sentence matching phrase from article content",
                "Another exact sentence matching phrase from article content"
            ]
        }}
    """

    try:
        response = gemini.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return safe_json_loads(
            response.text.strip(),
            default={
                "summary": "Linguistic analytics description generation suspended.",
                "reasons": [
                    "Gemini explanation generator encountered an unexpected execution timeout."
                ],
                "supporting_words": [],
                "opposing_words": [],
                "highlight_phrases": []
            }
        )

    except Exception as e:
        print(f"Gemini processing error: {str(e)}")
        return {
            "summary": "Linguistic analytics description generation suspended.",
            "reasons": [
                "Gemini explanation generator encountered an unexpected execution timeout."
            ],
            "supporting_words": [],
            "opposing_words": [],
            "highlight_phrases": []
        }