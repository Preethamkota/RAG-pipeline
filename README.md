# Local RAG API using FAISS + ollama

A Retrieval-Agumented Generation API that allows users to upload text / PDF / URL , and ask questions about the content using a local LLM (llama 3.2) 
This system extracts text , make small chunks out of it and make respective embeddings . These embeddings are stored in FAISS(Facebook AI Similarity Search) . retrieves relevant chunks and llm is used to generate a meaningful answer.

## Features:
- Upload raw text document
- Upload a PDF
- Upload a URL
- Extracts knowledge from them
- Converted to embeddings using nomic-embed-text
- Semantic search using FAISS
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


## Installation

### 1. Clone the repository

git clone https://github.com/your-username/RAG-pipeline
cd RAG-pipeline

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Download Ollama

Download and install Ollama from:
https://ollama.com

Then pull the required models:

ollama pull llama3.2
ollama pull nomic-embed-text

### 4. Run the FastAPI server

uvicorn main:app --reload

The API will start at : http://localhost:8000

And got to http://localhost:8000/static/index.html (UI of the website)

## Usage

1. Start the FastAPI server.

2. Open the UI:

http://localhost:8000/static/index.html

3. Upload content:
   - Raw text
   - PDF document
   - Website URL

4. Ask a question related to the uploaded content.

The system will:
- Convert the content into chunks
- Generate embeddings
- Store them in FAISS
- Retrieve the most relevant chunks
- Generate an answer using the LLM

## API Endpoints

### Upload Text

POST /upload

---

### Upload PDF

POST /upload-pdf

---

### Upload URL

POST /upload-url

---

### Ask Question

POST /ask
