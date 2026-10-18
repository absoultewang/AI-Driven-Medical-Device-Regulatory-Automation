FROM python:3.11-slim
WORKDIR /app
COPY crawler/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY crawler/ .
CMD ["python", "run_crawler.py"]
