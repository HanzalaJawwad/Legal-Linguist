# ⚖️ Legal-Linguist: AI Dispute Mediator

An automated dispute resolution portal built for my AI/ML portfolio. It uses **RAG (Retrieval-Augmented Generation)** to adjudicate buyer-seller conflicts based on specific Terms of Service.

## 🚀 Technical Highlights
- **Architecture:** RAG pipeline using LangChain and FAISS.
- **Reasoning:** Implements **Chain of Thought (CoT)** to detect logical fallacies (Ad Hominem, Emotional Appeals).
- **Frontend:** Streamlit for a clean, professional user interface.
- **Model:** Integrated with Gemini 1.5 Pro (Moving toward local Llama 3).

## 🛠️ Setup
1. Clone the repo: `git clone https://github.com/YOUR_USERNAME/Legal-Linguist.git`
2. Create venv: `python -m venv .venv`
3. Install: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`
