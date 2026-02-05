from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


import pdfplumber
import requests
from bs4 import BeautifulSoup

from rag_core import (
    ingest_document,
    retrieve_chunks,
    generate_answer
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

faiss_index = None
chunks = []



class Document(BaseModel):
    text: str


class Question(BaseModel):
    question: str


class URLRequest(BaseModel):
    url: str


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_text_from_url(url: str) -> str:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())



@app.get("/")
def root():
    return {"status": "RAG API running"}


# document
@app.post("/upload")
def upload_text(doc: Document):
    global faiss_index, chunks

    if not doc.text.strip():
        raise HTTPException(400, "Text is empty")

    faiss_index, chunks = ingest_document(doc.text)

    return {
        "message": "Text indexed successfully",
        "chunks_indexed": len(chunks),
        "preview": doc.text[:1000]
    }


# pdf
@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    global faiss_index, chunks

    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files allowed")

    text = extract_text_from_pdf(file.file)

    if not text.strip():
        raise HTTPException(400, "No text extracted from PDF")

    faiss_index, chunks = ingest_document(text)

    return {
        "message": "PDF indexed successfully",
        "chunks_indexed": len(chunks),
        "preview": text[:1000]
    }


# url
@app.post("/upload-url")
def upload_url(req: URLRequest):
    global faiss_index, chunks

    text = extract_text_from_url(req.url)

    if not text.strip():
        raise HTTPException(400, "No readable text found at URL")

    faiss_index, chunks = ingest_document(text)

    return {
        "message": "URL indexed successfully",
        "chunks_indexed": len(chunks),
        "preview": text[:1000]
    }


# question
@app.post("/ask")
def ask_question(q: Question):
    if faiss_index is None:
        raise HTTPException(400, "Upload content first")

    retrieved_chunks = retrieve_chunks(
        faiss_index,
        chunks,
        q.question,
        k=2
    )

    answer = generate_answer(q.question, retrieved_chunks)

    sources = [
        f'{c["source"]} – Chunk {c["chunk_id"]}'
        for c in retrieved_chunks
    ]

    return {
        "answer": answer,
        "sources": sources
    }
