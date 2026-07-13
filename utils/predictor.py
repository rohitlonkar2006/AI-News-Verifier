import numpy as np
from utils.config import (
    model,
    tokenizer,
    TITLE_MAX_LEN,
    TEXT_MAX_LEN,
    THRESHOLD
)
from utils.preprocessing import preprocess_inputs

def predict_news(title, article):
    title_pad, text_pad = preprocess_inputs(
        title,
        article,
        tokenizer,
        TITLE_MAX_LEN,
        TEXT_MAX_LEN
    )

    probability = model.predict(
        [title_pad, text_pad],
        verbose=0
    )[0][0]

    probability = float(probability)

    prediction = "REAL" if probability >= THRESHOLD else "FAKE"

    real_probability = round(probability * 100, 2)
    fake_probability = round((1.0 - probability) * 100, 2)

    confidence = round(max(real_probability, fake_probability), 2)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "threshold": round(THRESHOLD, 3),
        "real_probability": real_probability,
        "fake_probability": fake_probability,
        "raw_probability": probability
    }