AI PDF Summarizer and Q&A (RAG System)

This project implements an AI-powered system that allows users to upload a PDF document, generate a summary, and ask context-aware questions using Retrieval-Augmented Generation (RAG).

Features

- Upload PDF documents
- Extract text from PDF
- Split text into manageable chunks
- Generate embeddings for semantic search
- Store embeddings using FAISS
- Perform similarity-based retrieval
- Answer user queries based on document context
- Generate document summaries

Architecture Overview

User Upload (PDF)
        >
Text Extraction (PyMuPDF)
        >
Chunking (LangChain Text Splitter)
        >
Embeddings (Sentence Transformers)
        >
Vector Store (FAISS)
        >
User Query → Similarity Search
        >
Relevant Chunks → LLM (Groq)
        >
Final Answer

Tech Stack

Frontend: Streamlit
PDF Parsing: PyMuPDF
Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
Vector Database: FAISS
LLM: Groq (llama-3.1-8b-instant)
Chunking: LangChain Text Splitter

Project Structure

project/
├── app.py
├── rag_core.py
├── requirements.txt
├── .env

Setup Instructions

1. Clone the repository
git clone https://github.com/Gagansherigar/Ragchat
cd Ragchat

2. Create a virtual environment
python -m venv venv
source venv/bin/activate
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Set environment variables
GROQ_API_KEY=your_api_key_here

How to Run
streamlit run app.py

Usage

1. Upload a PDF
2. Choose summarization or Q&A
3. View results

Design Decisions and Trade-offs

1. FAISS for Vector Storage
FAISS was chosen for fast and efficient similarity search on embeddings.
Trade-off: FAISS is in-memory and does not persist data unless explicitly saved.

2. Sentence Transformers for Embeddings
The model all-MiniLM-L6-v2 is lightweight and fast.
Trade-off: Slightly lower semantic accuracy compared to larger embedding models.

3. Chunk-based Processing
Text is split into smaller chunks to improve retrieval accuracy.
Trade-off: More chunks lead to more LLM calls, increasing latency during summarization.

4. Groq LLM Integration
Groq provides fast inference for LLM responses.
Trade-off: Model availability may change and requires updating model names when deprecated.

5. Streamlit for Frontend
Streamlit allows rapid UI development with minimal code.
Trade-off: Limited scalability compared to full frontend frameworks like React.

---



Limitations

- PDF processing is done in-memory and not stored
- No support for scanned PDFs (OCR not implemented)
- Performance may degrade for very large documents
- No caching for embeddings across sessions

---

Security Notes

- API keys are stored in .env file and not committed
- Ensure .env is included in .gitignore
- Avoid exposing API keys in public repositories

---

Conclusion

This project demonstrates a complete end-to-end implementation of a Retrieval-Augmented Generation (RAG) system, integrating document processing, semantic search, and LLM-based question answering into a single application.