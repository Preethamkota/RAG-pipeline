import requests
import faiss
import numpy as np

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
OLLAMA_GEN_URL = "http://localhost:11434/api/generate"


#embedding
def embed_text(text: str) -> list:
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )
    return response.json()["embedding"]


#chunking
def chunk_text(text: str, sentences_per_chunk: int = 2) -> list:
    sentences = text.split(".")
    chunks = []
    current = []

    for s in sentences:
        s = s.strip()
        if not s:
            continue

        current.append(s)

        if len(current) == sentences_per_chunk:
            chunks.append(". ".join(current) + ".")
            current = []

    if current:
        chunks.append(". ".join(current) + ".")

    return chunks


#build faiss index
def build_faiss_index(embeddings: list):
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    return index


#ingest document
def ingest_document(text: str, source_name="Uploaded Text"):
    raw_chunks = chunk_text(text)

    chunks = []
    for i, chunk in enumerate(raw_chunks):
        chunks.append({
            "text": chunk,
            "source": source_name,
            "chunk_id": i
        })

    embeddings = [embed_text(c["text"]) for c in chunks]
    index = build_faiss_index(embeddings)

    return index, chunks


#retrieve chunks
def retrieve_chunks(index, chunks: list, question: str, k: int = 2):
    query_embedding = embed_text(question)
    query_vector = np.array([query_embedding]).astype("float32")

    _, indices = index.search(query_vector, k)

    retrieved = []
    for i in indices[0]:
        retrieved.append(chunks[i])

    return retrieved


#generate answer
def generate_answer(question: str, retrieved_chunks: list):
    context = "\n".join(c["text"] for c in retrieved_chunks)

    prompt = f"""
Answer ONLY using the context below.

Context:
{context}

Question:
{question}
"""

    response = requests.post(
        OLLAMA_GEN_URL,
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
