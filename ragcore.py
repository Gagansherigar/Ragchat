from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import fitz
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ------------------ Setup ------------------
load_dotenv()

if os.getenv("GROQ_API_KEY") is None:
    raise ValueError("GROQ_API_KEY not set")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------ Core Functions ------------------

def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)


def embed_chunks(chunks):
    return embed_model.encode(chunks)


def create_faiss_index(embeddings):
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index


def retrieve(query, index, chunks, k=3):
    query_embedding = embed_model.encode([query])
    _, indices = index.search(query_embedding, k)
    return [chunks[i] for i in indices[0]]


def generate_answer(context, question):
    prompt = f"""
    Answer ONLY from the context below.
    If not found, say "Not in document".

    Context:
    {context}

    Question:
    {question}
    """
    return llm.invoke(prompt).content


# ------------------ Summarization ------------------

def summarize_chunks(chunks):
    partial_summaries = []

    for chunk in chunks:
        prompt = f"Summarize this chunk in 3 bullet points:\n{chunk}"
        res = llm.invoke(prompt).content
        partial_summaries.append(res)

    final_prompt = f"""
    Combine these into a structured summary:
    - Overview
    - Key Points
    - Conclusion

    {partial_summaries}
    """

    return llm.invoke(final_prompt).content


# ------------------ Pipeline ------------------

def process_pdf(pdf_path):
    text = extract_text(pdf_path)
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    index = create_faiss_index(embeddings)

    return text, chunks, index
