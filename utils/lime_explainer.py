import numpy as np

from lime.lime_text import LimeTextExplainer

from utils.config import (
    model,
    tokenizer,
    TITLE_MAX_LEN,
    TEXT_MAX_LEN
)

from utils.preprocessing import preprocess_inputs



explainer = LimeTextExplainer(
    class_names=[
        "FAKE",
        "REAL"
    ]
)



def lime_predict(texts):

    probabilities = []

    for combined in texts:

        parts = combined.split("[SEP]")

        if len(parts) == 2:

            title = parts[0]

            article = parts[1]

        else:

            title = ""

            article = combined

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

        probabilities.append([

            1 - probability,

            probability

        ])

    return np.array(probabilities)



def explain_prediction(

    title,

    article,

    prediction

):

    combined = f"{title} [SEP] {article}"

    label = 1 if prediction == "REAL" else 0

    explanation = explainer.explain_instance(

        combined,

        lime_predict,

        labels=[label],

        num_features=10,

        num_samples=750

    )

    words = []

    for word, weight in explanation.as_list(label=label):

        words.append({

            "word": word,

            "weight": round(float(weight), 4)

        })

    return words