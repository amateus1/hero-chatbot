

# 🤖 AI Resume Chatbot

**`ai-resume-chatbot`** is an AI-powered, location-aware virtual assistant that represents **Al Mateus** — a global Agentic, LLM Engineering, MLOps and DevSecOps consultant — in an interactive, conversational format. Built using **Streamlit**, it dynamically serves resume information and switches between **OpenAI** and **DeepSeek** depending on user region (global vs. China).

[![CI/CD](https://github.com/yourusername/ai-resume-chatbot/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/ai-resume-chatbot/actions)
[![Streamlit App](https://img.shields.io/badge/Live%20App-Streamlit-orange?logo=streamlit)](https://yourapp.streamlit.app)

---

## 🧠 Features

- 🌍 **AI Resume Agent**: Chat with Al Mateus' professional experience via LLM.
- 🔁 **Smart LLM Switching**: Uses OpenAI outside China, DeepSeek inside.
- 🔒 **Secure Resume Files**: Loaded privately from AWS S3 (not public).
- 📬 **Notifications**: Resend for email, Pushover for mobile alerts.
- 🔐 **Secrets Managed**: Streamlit Secrets Manager handles all credentials.
- ⚙️ **CI/CD with GitHub Actions**: Linting, secret scanning, LLM API testing.

---

## 🛠️ Tech Stack

| Layer            | Tech                         |
|------------------|------------------------------|
| Frontend         | Streamlit                    |
| LLM APIs         | OpenAI GPT-4o, DeepSeek Chat |
| Backend Logic    | Python, PDF parsing, Boto3   |
| File Storage     | AWS S3 (private)             |
| Notifications    | Resend, Pushover             |
| CI/CD            | GitHub Actions               |

---

## 🚀 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/ai-resume-chatbot.git
cd ai-resume-chatbot

2. Install Requirements

pip install -r requirements.txt

3. Set Up Environment Variables

Add your credentials via environment variables or in Streamlit Cloud Secrets:

OPENAI_API_KEY = "sk-..."
DEEPSEEK_API_KEY = "..."
AWS_ACCESS_KEY_ID = "..."
AWS_SECRET_ACCESS_KEY = "..."
AWS_REGION = "us-east-1"
S3_BUCKET = "your-bucket-name"
SUMMARY_KEY = "me/summary.txt"
LINKEDIN_KEY = "me/linkedin.pdf"
RESEND_API_KEY = "..."
PUSHOVER_TOKEN = "..."
PUSHOVER_USER = "..."

4. Run Locally

streamlit run app.py

📄 Project Structure

├── app.py                 # Streamlit frontend
├── me_chatbot.py          # Chat logic & API switching
├── requirements.txt       # Python dependencies
├── tests/
│   ├── test_openai.py
│   └── test_deepseek.py
└── .github/workflows/
    └── ci.yml             # GitHub Actions CI/CD pipeline

🧪 CI/CD (GitHub Actions)

This repo uses GitHub Actions to:

    ✅ Lint code with flake8 and black

    ✅ Scan for committed secrets with detect-secrets

    ✅ Test OpenAI and DeepSeek API access

View CI results: CI Dashboard
🌐 Live Demo

Try the app live: yourname.me

    (or Streamlit URL: https://almateus.me)

📜 License

MIT License — use, modify, and share freely.
🤝 Contact

Built by Al Mateus
✉️ al@optimops.ai
🌐 LinkedIn


---



