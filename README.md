# RAG Document Chatbot

A chatbot that lets you upload your own documents and ask questions about them. Built this to learn how RAG (Retrieval-Augmented Generation) works in practice.

## What it does
- Upload PDF, TXT, or DOCX files
- Ask questions about the content
- Get answers with page-level source citations
- Supports multiple documents at once

## How it works
Instead of sending the whole document to an LLM (which hits token limits), it do :
1. Splits the document into chunks
2. Converts each chunk into a vector embedding (used HuggingFace all-MiniLM-L6-v2)
3. Stores them in a FAISS vector index
4. On each query, finds the 4 most relevant chunks and sends only those to the LLM

## Tech Stack
- **LangChain** – document loading and text splitting
- **FAISS** – vector similarity search
- **HuggingFace Embeddings** – all-MiniLM-L6-v2 (384 dimensions)
- **Groq API** – LLaMA 3.3-70B as the LLM
- **Streamlit** – UI

## Setup

```bash / terminal 
pip install langchain langchain-huggingface faiss-cpu groq streamlit python-docx
```

Add your Groq API key as an environment variable:
```bash / terminal 
export GROQ_API_KEY=your_key_here
```

Run:
```bash / terminal 
python -m streamlit run app.py
```

## Things I learned
- Why chunking strategy matters (chunk size vs overlap tradeoffs)
- How vector similarity search works under the hood
- Why the same embedding model must be used at ingest and query time
- RAG is great for Q&A but not for full document summarization
