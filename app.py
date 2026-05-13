import streamlit as st
import json
import tempfile

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="AI Mediator", layout="wide")

st.title("⚖️ AI Dispute Resolution Portal")
st.markdown("---")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🛠 Admin Panel")

uploaded_tos = st.sidebar.file_uploader(
    "Store Terms of Service (PDF)",
    type=["pdf"]
)

# =========================
# MAIN UI
# =========================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛒 Buyer Claim")
    buyer_claim = st.text_area(
        "What happened?",
        height=300
    )

with col2:
    st.subheader("🏬 Seller Defense")
    seller_defense = st.text_area(
        "What is your response?",
        height=300
    )

# =========================
# IMPORTS
# =========================
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# =========================
# PDF PROCESSING
# =========================
def process_pdf(uploaded_file):

    # Save uploaded PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    # Load PDF
    loader = PyPDFLoader(temp_path)
    docs = loader.load()

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    split_docs = splitter.split_documents(docs)

    # Embeddings
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    # Vector DB
    vectorstore = FAISS.from_documents(
        split_docs,
        embeddings
    )

    retriever = vectorstore.as_retriever()

    return retriever

# =========================
# VERDICT GENERATION
# =========================
def generate_verdict(retriever, buyer_text, seller_text):

    llm = OllamaLLM(
        model="phi3",
        temperature=0
    )

    template = """
You are a professional Legal Mediator.

Use ONLY the provided policy context.

Ignore emotional arguments.

Return ONLY valid JSON.

JSON FORMAT:
{{
    "winner": "Buyer or Seller",
    "policy_reference": "Referenced rule",
    "reasoning": "Why this side wins"
}}

Context:
{context}

Question:
{question}
"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={
            "prompt": prompt
        },
        return_source_documents=False
    )

    dispute = f"""
Buyer Claim:
{buyer_text}

Seller Defense:
{seller_text}
"""

    # IMPORTANT FIX
    result = qa_chain.invoke({
        "query": dispute
    })

    return result["result"]

# =========================
# BUTTON
# =========================
if st.button("Generate Verdict", use_container_width=True):

    if not uploaded_tos:
        st.warning("Please upload the Terms of Service PDF.")
    elif not buyer_claim or not seller_defense:
        st.warning("Please fill both Buyer Claim and Seller Defense.")
    else:

        raw_result = ""

        with st.spinner("AI is analyzing the dispute..."):

            try:
                retriever = process_pdf(uploaded_tos)

                raw_result = generate_verdict(
                    retriever,
                    buyer_claim,
                    seller_defense
                )

                # Clean markdown if model adds ```json
                cleaned = raw_result.replace("```json", "").replace("```", "").strip()

                verdict = json.loads(cleaned)

                st.markdown("---")

                if verdict["winner"].lower() == "buyer":
                    st.success(f"### Verdict: Favor {verdict['winner']}")
                else:
                    st.error(f"### Verdict: Favor {verdict['winner']}")

                st.info(
                    f"**Policy Reference:** {verdict['policy_reference']}"
                )

                st.write(
                    f"**Reasoning:** {verdict['reasoning']}"
                )

            except json.JSONDecodeError:
                st.error("Model did not return valid JSON.")
                st.code(raw_result)

            except Exception as e:
                st.error(f"Error: {e}")

                if raw_result:
                    st.code(raw_result)