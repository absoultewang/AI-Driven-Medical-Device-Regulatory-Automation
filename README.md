# PoC for AI-Driven Medical Device Regulatory Automation

This branch contains a minimal PoC stack to ingest regulatory documents, parse/OCR PDFs, index into a vector DB (Milvus) and a full-text search (OpenSearch), and provide a simple RAG API.

## Quick start (development)

1. Clone repo and checkout branch:

   git checkout poc/initial-setup

2. Start services:

   docker compose up -d

3. Build and run backend/frontend if needed (or use the images built by compose)

4. Ingest a sample PDF:

   docker compose exec fastapi python ingest.py /path/to/sample.pdf

5. Query the RAG endpoint (example):

   curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question":"某产品需要哪些注册资料？"}'

## Notes
- The PoC uses placeholder embedding and LLM endpoints. Replace `EMBED_ENDPOINT` and `LLM_ENDPOINT` with your model endpoints or local inference service.
- For Chinese OCR and scanned PDFs, PaddleOCR is included in requirements; for production tune models and consider GPU.

## Resources
- Milvus: https://milvus.io
- OpenSearch: https://opensearch.org
- LangChain / LlamaIndex: integrate in backend for advanced pipeline

