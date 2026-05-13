# ⚖️ Legal-Linguist — AI Dispute Resolution Portal

Legal-Linguist is an AI-powered dispute mediation system that analyzes buyer–seller conflicts using Retrieval-Augmented Generation (RAG), policy reasoning, and local LLM inference.

The system evaluates disputes strictly based on uploaded Terms of Service documents and generates structured legal-style verdicts while ignoring emotional manipulation and logical fallacies.

---

# 🚀 Features

- 📄 Upload custom Terms of Service PDFs
- 🤖 AI-generated legal verdicts
- ⚖️ Policy-based reasoning using RAG
- 🧠 Detects emotional appeals and irrelevant arguments
- 🔍 Semantic document retrieval with FAISS
- 🖥️ Modern Streamlit interface
- 🔒 Fully local LLM execution using Ollama
- 📦 JSON-based structured verdict generation

---

# 🧠 Tech Stack

## Frontend
- Streamlit

## AI / Backend
- LangChain
- Ollama
- FAISS Vector Database
- Recursive Character Text Splitting
- RAG (Retrieval-Augmented Generation)

## Models
- `phi3` — dispute reasoning
- `nomic-embed-text` — embeddings

---

# ⚙️ How It Works

1. Upload a Terms of Service PDF
2. Buyer enters a dispute claim
3. Seller enters their defense
4. The AI:
   - extracts relevant policy clauses,
   - retrieves related context,
   - evaluates both sides,
   - ignores emotional fallacies,
   - returns a structured verdict.

---

# 🛠️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/HanzalaJawwad/Legal-Linguist.git
cd Legal-Linguist
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install Ollama

Download and install Ollama:

[Ollama Official Website](https://ollama.com?utm_source=chatgpt.com)

---

## 5. Pull Required Models

```bash
ollama pull phi3
ollama pull nomic-embed-text
```

---

## 6. Run the Application

```bash
streamlit run app.py
```

---

# 📂 Project Structure

```text
Legal-Linguist/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── assets/
```

---

# 📸 Screenshots

Add screenshots of:
- dispute interface
- generated verdicts
- policy extraction
- admin PDF upload panel

---

# 🔮 Planned Improvements

- Multi-agent legal reasoning
- Memory-based dispute tracking
- Voice-based dispute input
- Support for multiple legal jurisdictions
- Fine-tuned legal LLM
- Export verdicts as PDF
- Authentication system
- Docker deployment

---

# 🧪 Example Use Cases

- E-commerce dispute mediation
- Marketplace refund validation
- AI legal assistant prototypes
- Customer support automation
- Policy compliance systems

---

# ⚠️ Disclaimer

This project is for educational and research purposes only.

It is not a substitute for professional legal advice.

---

# 👨‍💻 Author

Hanzala Jawwad

- AI/ML Developer
- Software Engineer
- UI/UX Designer
- Hackathon Organizer 

GitHub:
[HanzalaJawwad GitHub Profile](https://github.com/HanzalaJawwad?utm_source=chatgpt.com)

---

# ⭐ Support

If you like this project:
- Star the repository
- Fork the project
- Contribute improvements
- Share feedback
