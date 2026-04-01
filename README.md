# 🔍 Internship Scam Detector

An AI-powered web application that detects fake internship and job postings using Machine Learning, NLP, and multi-factor analysis.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![ML](https://img.shields.io/badge/ML-Scikit--learn-orange)

---

## 🚀 Features

- **ML Model** - Trained on 27,566 job postings (Logistic Regression + Sentence Transformers)
- **Text Analysis** - Suspicious phrases, urgency, emotion, grammar detection
- **Website Checker** - SSL, domain, content analysis
- **LinkedIn Validator** - Profile existence and URL verification
- **Screenshot OCR** - Extracts and analyzes text from images (Tesseract)
- **Multi-page Frontend** - Home, About, Awareness, Analyzer pages

---

## 📁 Project Structure

```
internship-scam-detector/
├── backend/
│   └── app/
│       ├── main.py              # FastAPI app entry point
│       ├── routes/
│       │   ├── analyze.py       # Main analysis endpoint
│       │   └── reports.py       # Reports endpoint
│       └── services/
│           ├── ml_model.py      # ML model loader & predictor
│           ├── text_checker.py  # Text + ML analysis
│           ├── scam_score.py    # Score aggregation
│           ├── nlp_features.py  # Urgency, emotion, grammar
│           ├── website_checker.py
│           ├── linkedin_checker.py
│           └── image_ocr.py     # Tesseract OCR
├── frontend/
│   ├── home.html
│   ├── about.html
│   ├── awareness.html
│   ├── analyzer.html
│   └── styles.css
├── models/
│   └── job_scam_classifier.pkl  # Trained classifier
├── train_simple.py              # Script to train & save models
├── requirements.txt
└── render.yaml                  # Render deployment config
```

---

## ⚙️ Local Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the model (first time only)
```bash
python train_simple.py
```

### 3. Start the backend
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Start the frontend
```bash
python -m http.server 3000 --directory frontend
```

Open: **http://localhost:3000**

---

## 🌐 Deployment on Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. Deploy!

After deployment, update `API_URL` in `frontend/analyzer.html`:
```js
const API_URL = 'https://your-app-name.onrender.com';
```

---

## 🧠 Model Details

| Component | Details |
|-----------|---------|
| Algorithm | Logistic Regression |
| Embeddings | all-MiniLM-L6-v2 (Sentence Transformers) |
| Training Data | 27,566 job postings |
| Features | title, description, requirements, benefits, company_profile, employment_type, industry |
| Accuracy | 95%+ |

---

## 📊 Scoring System

| Score | Verdict |
|-------|---------|
| 0 - 34 | ✅ Safe |
| 35 - 59 | ⚠️ Suspicious |
| 60 - 100 | 🚨 Likely Scam |

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **ML:** Scikit-learn, Sentence Transformers, Joblib
- **OCR:** Tesseract, OpenCV, Pillow
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
