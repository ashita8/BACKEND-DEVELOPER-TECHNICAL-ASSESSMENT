from fastapi import FastAPI
from database import engine
from models.customer import Base
from services.ingestion import fetch_all ,upsert_customers

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test-fetch")
def test_fetch():
    data = fetch_all()
    return {"count": len(data)}

@app.post("/api/ingest")
def ingest():
    data = fetch_all()
    upsert_customers(data)

    return {
        "status": "success",
        "records_processed": len(data)
    }