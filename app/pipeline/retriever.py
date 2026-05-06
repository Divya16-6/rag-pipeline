from app.pipeline.embedder import embed
from app.pipeline.pinecone_store import init_index

def retrieve(query, top_k=3):
    query_vec = embed([query])[0]
    index = init_index(len(query_vec))

    result = index.query(vector=query_vec, top_k=top_k, include_metadata=True)

    return [match["metadata"]["text"] for match in result["matches"]]