from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()
EMBED_ENDPOINT = "http://localhost:8080/embed"
LLM_ENDPOINT = "http://localhost:8080/llm"

class Query(BaseModel):
    question: str
    top_k: int = 5

@app.post("/query")
def query(q: Query):
    emb = requests.post(EMBED_ENDPOINT, json={"text": q.question}).json().get("embedding")
    # Placeholder for milvus/opensearch retrieval
    contexts = [{"doc_id":"demo","score":0.9,"text":"示例证据段落（来自法规）"}]
    prompt = "Use the following contexts to answer and include source ids:\n\n" + "\n\n".join([c["text"] for c in contexts]) + f"\n\nQuestion: {q.question}"
    llm_resp = requests.post(LLM_ENDPOINT, json={"prompt": prompt}).json()
    return {"answer": llm_resp.get("text"), "sources": contexts}
