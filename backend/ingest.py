"""
Minimal PoC ingest: parse PDF -> text -> embeddings -> milvus + opensearch
Requires: pdfplumber, paddleocr (or tesseract), request to embedding model, pymilvus, opensearch-py
"""
import os
import hashlib
import pdfplumber
from paddleocr import PaddleOCR
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from opensearchpy import OpenSearch
import requests

MILVUS_HOST = os.getenv("MILVUS_HOST", "milvus")
MILVUS_PORT = int(os.getenv("MILVUS_PORT", 19530))
OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "opensearch")
EMBED_ENDPOINT = os.getenv("EMBED_ENDPOINT", "http://localhost:8080/embed")

ocr = PaddleOCR(use_angle_cls=True, lang='ch')

# Connect milvus
connections.connect("default", host=MILVUS_HOST, port=str(MILVUS_PORT))
fields = [
    FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=256, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)
]
schema = CollectionSchema(fields, "doc vector collection")
collection_name = "poc_docs"
if collection_name not in Collection.list_collections():
    coll = Collection(name=collection_name, schema=schema)
else:
    coll = Collection(collection_name)

os_client = OpenSearch(hosts=[{'host': OPENSEARCH_HOST, 'port': 9200}])
index_name = "poc_documents"
if not os_client.indices.exists(index=index_name):
    os_client.indices.create(index=index_name)


def file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def extract_text_from_pdf(path):
    text_pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            text_pages.append(text)
    return "\n\n".join(text_pages)


def ocr_image(path):
    result = ocr.ocr(path, cls=True)
    lines = []
    for r in result:
        for line in r:
            lines.append(line[1][0])
    return "\n".join(lines)


def embed_text(text):
    resp = requests.post(EMBED_ENDPOINT, json={"text": text})
    return resp.json().get("embedding")


def ingest_file(path, metadata=None):
    doc_id = file_hash(path)
    text = extract_text_from_pdf(path)
    if (not text.strip()):
        text = ocr_image(path)
    embedding = embed_text(text)
    coll.insert([[doc_id], [embedding]])
    doc = {"doc_id": doc_id, "text": text[:10000], "metadata": metadata or {}}
    os_client.index(index=index_name, id=doc_id, body=doc)
    print("Ingested", path, doc_id)

if __name__ == "__main__":
    import sys
    p = sys.argv[1]
    ingest_file(p, metadata={"source":"demo"})
