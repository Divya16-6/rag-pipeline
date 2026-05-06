from pinecone import Pinecone, ServerlessSpec
from app.utilis.config import PINECONE_API_KEY, PINECONE_ENV, INDEX_NAME

pc = Pinecone(api_key=PINECONE_API_KEY)

def init_index(dimension):
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_ENV
            )
        )

    return pc.Index(INDEX_NAME)


def upsert_vectors(index, chunks, embeddings):
    vectors = []

    for i, chunk in enumerate(chunks):
        vectors.append({
            "id": str(i),
            "values": embeddings[i],
            "metadata": {"text": chunk.page_content}
        })

    index.upsert(vectors=vectors)