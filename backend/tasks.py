from celery import Celery
from ingest import ingest_file

app = Celery('tasks', broker='redis://redis:6379/0')

@app.task
def parse_and_index(path, metadata=None):
    ingest_file(path, metadata)
