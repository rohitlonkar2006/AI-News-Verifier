from utils.predictor import predict_news
from utils.gemini_service import generate_explanation

def build_response(title, article):
    prediction = predict_news(title, article)

    gemini_output = generate_explanation(
        title,
        article,
        prediction["prediction"],
        prediction["confidence"]
    )

    return {
        "success": True,
        "title": title,
        "article": article,
        "prediction": prediction["prediction"],
        "confidence": prediction["confidence"],
        "threshold": prediction["threshold"],
        "real_probability": prediction["real_probability"],
        "fake_probability": prediction["fake_probability"],
        "raw_probability": prediction["raw_probability"],
        "summary": gemini_output.get("summary", "Executive summary explanation suspended."),
        "reasons": gemini_output.get("reasons", ["Context analytics compilation failed."]),
        "highlight_phrases": gemini_output.get("highlight_phrases", []),
        "supporting_words": gemini_output.get("supporting_words", []),
        "opposing_words": gemini_output.get("opposing_words", [])
    }