# 📰 AI Fake News Detector

An AI-powered web application that analyzes news articles and predicts whether they are **Real** or **Fake** using a custom **BiLSTM-based Deep Learning model** with an **Attention mechanism**. The platform supports both **URL-based news extraction** and **manual article input**, providing confidence scores, AI-assisted explanations, and a modern responsive dashboard.


https://github.com/user-attachments/assets/e11f5751-66b1-4a48-8266-f3f8e825776a


---

# ⭐ Highlights

- 🧠 Custom **BiLSTM + Attention** architecture
- 📚 Pre-trained **GloVe (100D)** word embeddings
- 🎯 Optimized prediction threshold (**0.53**) using validation-set threshold tuning
- 📊 **97.41% Test Accuracy**
- 📈 **99.58% ROC-AUC**
- 🌐 URL-based article extraction
- ✍️ Manual article verification
- 🤖 Google Gemini 2.5 Flash AI-assisted explanations
- 💻 Responsive Flask web application

---

# 🚀 Features

### 🔍 Dual-Input Analysis

Processes the **news headline** and **article body** separately, allowing the model to capture differences between sensational headlines and actual article content.

---

### 🧠 Deep Learning Classifier

- Custom BiLSTM + Attention architecture
- Shared GloVe embeddings
- Threshold optimized to **0.53** for maximum F1-score
- Binary classification (Real / Fake)

---

### 🤖 AI-Assisted Explanation

Google Gemini 2.5 Flash generates:

- Executive summary
- Credibility indicators
- Important highlighted phrases
- Human-readable explanation of the prediction

---

### 🌐 URL News Analyzer

Automatically extracts readable news content from supported websites before sending it to the model.

---

### ✍️ Manual Article Verification

Users can manually enter any headline and article for instant prediction.

---

### 📊 Interactive Dashboard

- Prediction badge
- Confidence score
- Real/Fake probability bars
- AI-generated summary
- Responsive modern UI

---

### ⚡ Client-side Validation

- URL validation
- Empty field validation
- Input sanitization

---

# 🧠 Model Architecture

The classification model consists of:

- Shared GloVe Embedding Layer (100D)
- Bidirectional LSTM
- Custom Attention Layer
- Fully Connected Dense Layers
- Sigmoid Output Layer

### Training Configuration

- Optimizer: AdamW
- Loss: Binary Crossentropy with Label Smoothing
- Mixed Precision Training
- Early Stopping
- ReduceLROnPlateau
- Threshold Optimization

---

# 📊 Model Performance

| Metric | Score |
|---------|--------|
| Accuracy | **97.41%** |
| Precision | **97.04%** |
| Recall | **97.58%** |
| F1 Score | **97.31%** |
| ROC-AUC | **99.58%** |
| PR-AUC | **99.52%** |

---

# 📂 Dataset

The model was trained on a combined **Fake and Real News Dataset** containing over **270,000** news articles.

Each record contains:

- News Title
- News Article
- Binary Label (Real / Fake)

Preprocessing steps included:

- Duplicate removal
- Missing value handling
- Text normalization
- Tokenization
- Sequence padding
- GloVe embedding initialization

---

# ⚙️ System Workflow

```text
                News URL / Manual Input
                         │
                         ▼
              Content Extraction (APYHub)
                         │
                         ▼
                Text Preprocessing
                         │
                         ▼
      Headline + Article Tokenization
                         │
                         ▼
         BiLSTM + Attention Network
                         │
                         ▼
          Real / Fake Prediction
                         │
                         ▼
     Gemini AI Explanation Generator
                         │
                         ▼
        Interactive Web Dashboard
```

---

# 📁 Project Structure

```text
AI-News-Verifier/
│
├── app.py
├── requirements.txt
├── .env
│
├── models/
│   ├── fake_news_bilstm_v2.keras
│   ├── tokenizer.pkl
│   ├── max_lengths.pkl
│   └── threshold.pkl
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── app.js
│
├── templates/
│   └── index.html
│
└── utils/
    ├── config.py
    ├── preprocessing.py
    ├── predictor.py
    ├── scraper.py
    ├── gemini_service.py
    ├── response_builder.py
    └── lime_explainer.py
```

---

# 🛠 Installation

## Clone Repository

```bash
git clone https://github.com/deepsurude0902/AI-News-Verifier.git

cd AI-News-Verifier
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
APYHUB_API_KEY=YOUR_APYHUB_API_KEY
```

> **Important:** Never commit your `.env` file to GitHub.

---

# ▶️ Run the Project

```bash
python app.py
```

The application will start at:

```
http://127.0.0.1:5000
```

---

# 💻 Usage

## 🌐 URL Analysis

1. Paste a news article URL.
2. Click **Analyze**.
3. The application extracts the article.
4. The deep learning model predicts whether it is Real or Fake.
5. Gemini generates an AI-assisted explanation.

---

## ✍️ Manual Analysis

1. Open the **Manual Input** tab.
2. Enter the news headline.
3. Paste the article content.
4. Click **Verify**.
5. View the prediction, confidence score, probabilities, and AI explanation.

---

# 🧰 Technologies Used

### Machine Learning

- TensorFlow / Keras
- BiLSTM
- Custom Attention Layer
- GloVe Word Embeddings
- Scikit-learn

### Backend

- Flask
- Python
- BeautifulSoup
- Requests

### Frontend

- HTML5
- CSS3
- JavaScript

### APIs

- Google Gemini 2.5 Flash API
- APYHub Web Extraction API

---

# 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify, distribute, and build upon this project for both personal and commercial purposes, provided that the original copyright notice and this license are included.

---

# 👨‍💻 Author

**Deep Surude**

B.Tech CSE (Artificial Intelligence & Analytics)

MIT ADT University, Pune

**GitHub:** https://github.com/deepsurude0902
