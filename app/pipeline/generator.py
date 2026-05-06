def generate(query, chunks):
    context = "\n".join(chunks)

    return f"""
Context:
{context}

Question:
{query}

Answer:
"""