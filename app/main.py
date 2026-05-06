from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil, os

from app.pipeline.loader import load_pdf
from app.pipeline.cleaner import clean_docs
from app.pipeline.chunker import chunk_docs
from app.pipeline.embedder import embed
from app.pipeline.pinecone_store import init_index, upsert_vectors
from app.pipeline.retriever import retrieve
from app.pipeline.generator import generate

from app.utilis.language import detect_language, translate
from app.utilis.config import UPLOAD_PATH

app = FastAPI(title="RAG Pinecone API")


class QueryRequest(BaseModel):
    question: str


@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    os.makedirs("data", exist_ok=True)

    with open(UPLOAD_PATH, "wb") as f:
        shutil.copyfileobj(file.file, f)

    docs = load_pdf(UPLOAD_PATH)
    docs = clean_docs(docs)
    chunks = chunk_docs(docs)

    texts = [c.page_content for c in chunks]
    embeddings = embed(texts)

    index = init_index(len(embeddings[0]))
    upsert_vectors(index, chunks, embeddings)

    return {"message": "Data indexed in Pinecone"}


@app.post("/query")
def query(req: QueryRequest):

    # Detect language
    lang = detect_language(req.question)

    # Translate to English
    q_en = translate(req.question, lang, "en")

    # Retrieve
    chunks = retrieve(q_en)

    # Generate answer
    answer_en = generate(q_en, chunks)

    # Translate back
    final_answer = translate(answer_en, "en", lang)

    return {
        "detected_language": lang,
        "answer": final_answer,
        "chunks": chunks
    }