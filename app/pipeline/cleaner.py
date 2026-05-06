import re

def clean_docs(docs):
    for d in docs:
        d.page_content = re.sub(r"\s+", " ", d.page_content).strip()
    return docs