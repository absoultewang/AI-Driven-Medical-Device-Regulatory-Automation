# Updated notes: mock model automatically included in docker-compose

The mock model exposes two endpoints used by the PoC back-end:
- POST /embed {"text": "..."} -> {"embedding": [float,...]}
- POST /llm {"prompt": "..."} -> {"text": "..."}

This service is intended only for PoC/demo purposes. Replace with real embedding
and LLM services for production workloads.
