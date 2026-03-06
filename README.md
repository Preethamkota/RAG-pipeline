# Local RAG API using FAISS + ollama

A Retrieval-Augumented Generation API that allows users to upload text / PDF / URL , and ask questions about the content using a local LLM (llama 3.2) 
This system extracts text , make small chunks out of it and make respective embeddings . These embeddings are stored in FAISS(Facebook AI Similarity Search) . retrieves relevant chunks and llm is used to generate a meaningful answer.

## Features:
- Upload raw text document
- Upload a PDF
- Upload a URL
- Extracts knowledge from them
- Converted to embeddings using nomic-embed-text
- Sematic search using FAISS
- Answer generation using llama3.2

## Architecture

User Content
      ↓
Text Extraction (PDF / URL)
      ↓
Chunking
      ↓
Embedding (nomic-embed-text)
      ↓
FAISS Vector Index
      ↓
Query Embedding
      ↓
Similarity Search
      ↓
LLM Generation (llama3.2)
      ↓
Final Answer


## Tech Stack

- **Backend:** FastAPI
- **Vector Database:** FAISS
- **Embeddings:** Ollama (nomic-embed-text)
- **LLM:** Ollama (llama3.2)
- **PDF Parsing:** pdfplumber
- **Web Scraping:** BeautifulSoup
- **Language:** Python
