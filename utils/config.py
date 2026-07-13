import os
import pickle
import google.generativeai as genai
import tensorflow as tf
from dotenv import load_dotenv
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import custom_object_scope

from utils.preprocessing import AttentionLayer

load_dotenv()

APYHUB_API_KEY = os.getenv("APYHUB_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("gemini-2.5-flash")


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "fake_news_bilstm_v2.keras")
TOKENIZER_PATH = os.path.join(MODEL_DIR, "tokenizer.pkl")
MAX_LENGTH_PATH = os.path.join(MODEL_DIR, "max_lengths.pkl")
THRESHOLD_PATH = os.path.join(MODEL_DIR, "threshold.pkl")

with custom_object_scope({"AttentionLayer": AttentionLayer}):
    model = load_model(
        MODEL_PATH,
        compile=False
    )

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)

with open(MAX_LENGTH_PATH, "rb") as f:
    max_lengths = pickle.load(f)

TITLE_MAX_LEN = max_lengths["TITLE_MAX_LEN"]
TEXT_MAX_LEN = max_lengths["TEXT_MAX_LEN"]

with open(THRESHOLD_PATH, "rb") as f:
    THRESHOLD = pickle.load(f)

print("=" * 60)
print("Model Loaded Successfully with 3-Param Attention Architecture")
print("Verified Threshold :", THRESHOLD)
print("=" * 60)