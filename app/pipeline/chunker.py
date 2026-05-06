from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.utilis.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_documents(docs)