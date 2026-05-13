import streamlit as st
import os
import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# --- Configuration & Styling ---
st.set_page_config(layout="wide", page_title="AI Dispute Mediator")

# Ensure you have your API Key set in your environment or enter it here
# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

# --- Step 3: The RAG Pipeline (Ingestion Logic) ---
def process_pdf(uploaded_file):
    """Extracts text from PDF, chunks it, and creates a FAISS vector store."""
    # Save temp file to disk for PyPDFLoader
    with open("temp_tos.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    loader = PyPDFLoader("temp_tos.pdf")
    pages = loader.load()
    
    # AI/ML Note: 500/50 split is great for maintaining context in legal clauses
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(pages)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store.as_retriever()

# --- Step 4: The Reasoning Engine ---
def generate_verdict(retriever, buyer_text, seller_text):
    """Executes Chain of Thought reasoning to generate a JSON verdict."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
    
    template = """
    SYSTEM: You are a professional Legal Mediator. Your goal is to resolve disputes based STRICTLY on the provided Terms of Service (ToS).
    
    REASONING PROTOCOL:
    1. IDENTIFY FALLACIES: Scan both claims for logical fallacies (ad hominem, red herrings, emotional manipulation).
    2. CONSULT POLICY: Retrieve specific clauses from the ToS that apply to the situation.
    3. NEUTRAL ADJUDICATION: Compare the facts against the policy. Ignore non-contractual pleas.
    
    OUTPUT FORMAT: You must return ONLY a JSON object with these keys:
    {
        "winner": "Buyer" or "Seller",
        "policy_reference": "Specific clause or rule found",
        "reasoning": "Step-by-step breakdown of your decision"
    }

    CONTEXT (ToS): {context}
    
    DISPUTE DETAILS:
    Buyer Claim: {buyer_claim}
    Seller Defense: {seller_defense}
    
    JSON VERDICT:
    """
    
    prompt = PromptTemplate(
        template=template, 
        input_variables=["context", "buyer_claim", "seller_defense"]
    )
    
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )
    
    response = chain.invoke({
        "query": f"Analyze this dispute: Buyer: {buyer_text} vs Seller: {seller_text}",
        "buyer_claim": buyer_text,
        "seller_defense": seller_text
    })
    
    return response["result"]

# --- UI Scaffolding ---
st.sidebar.title("🛠 Admin Panel")
uploaded_tos = st.sidebar.file_uploader("Store Terms of Service (PDF)", type=["pdf"])

st.title("⚖️ AI Dispute Resolution Portal")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🛒 Buyer Claim")
    buyer_claim = st.text_area("What happened?", height=300, placeholder="Describe your issue...")

with col2:
    st.subheader("🏬 Seller Defense")
    seller_defense = st.text_area("What is your response?", height=300, placeholder="Describe your defense...")

if st.button("Generate Verdict", use_container_width=True):
    if not uploaded_tos:
        st.warning("Please upload the Terms of Service PDF in the sidebar first.")
    elif not buyer_claim or not seller_defense:
        st.warning("Both parties must provide a statement.")
    else:
        with st.spinner("Analyzing claims and cross-referencing policy..."):
            try:
                # 1. Build/Retrieve Vector Store
                retriever = process_pdf(uploaded_tos)
                
                # 2. Run Reasoning Engine
                raw_result = generate_verdict(retriever, buyer_claim, seller_defense)
                
                # 3. Parse and Display
                verdict = json.loads(raw_result)
                
                st.markdown("---")
                if verdict['winner'] == "Buyer":
                    st.success(f"### Verdict: Favor {verdict['winner']}")
                else:
                    st.error(f"### Verdict: Favor {verdict['winner']}")
                
                st.info(f"**Policy Referenced:** {verdict['policy_reference']}")
                st.write(f"**Reasoning:** {verdict['reasoning']}")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")