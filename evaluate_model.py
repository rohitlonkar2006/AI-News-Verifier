import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from utils.predictor import predict_news

# Load datasets
fake_df = pd.read_csv("data/Fake.csv")
true_df = pd.read_csv("data/True.csv")

# Add labels
fake_df["label"] = "FAKE"
true_df["label"] = "REAL"

# Combine datasets
df = pd.concat([fake_df, true_df], ignore_index=True)

# Optional: evaluate on a subset first
df = df.sample(n=1000, random_state=42)

true_labels = []
predicted_labels = []

print("Evaluating model...\n")

for _, row in df.iterrows():
    try:
        result = predict_news(
            str(row["title"]),
            str(row["text"])
        )

        predicted_labels.append(result["prediction"])
        true_labels.append(row["label"])

    except Exception as e:
        print(f"Error: {e}")

print("\n========== RESULTS ==========\n")

print(f"Accuracy : {accuracy_score(true_labels, predicted_labels)*100:.2f}%")
print(f"Precision: {precision_score(true_labels, predicted_labels, average='weighted')*100:.2f}%")
print(f"Recall   : {recall_score(true_labels, predicted_labels, average='weighted')*100:.2f}%")
print(f"F1 Score : {f1_score(true_labels, predicted_labels, average='weighted')*100:.2f}%")

print("\nClassification Report\n")
print(classification_report(true_labels, predicted_labels))

print("\nConfusion Matrix\n")
print(confusion_matrix(true_labels, predicted_labels))