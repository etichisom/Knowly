from fastapi import FastAPI
from sqlalchemy import text

from app.db import engine

app = FastAPI(title="Knowly")
# uvicorn app.main:app --reload ---> run app

@app.get('/health')
def health():
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    return {'status':'ok','database':'ok'}