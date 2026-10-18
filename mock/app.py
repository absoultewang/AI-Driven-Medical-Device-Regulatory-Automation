from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class TextIn(BaseModel):
    text: str

@app.post('/embed')
def embed(payload: TextIn):
    # deterministic mock embedding: hash-based pseudo-vector
    vec = [0.001 * ((hash(payload.text) >> i) & 255) for i in range(768)]
    return {'embedding': vec}

@app.post('/llm')
def llm(payload: dict):
    prompt = payload.get('prompt') or payload.get('text') or ''
    # simple mock reply that includes a short summary and echoes source ids if present
    reply = '（Mock LLM 回答）根据提供的上下文，生成以下简要结论。\n\n' + (prompt[:500] + '...')
    return {'text': reply}
