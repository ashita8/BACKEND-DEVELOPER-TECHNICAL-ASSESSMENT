import requests
from fastapi import FastAPI
from database import engine
from models.customer import Base
from services.ingestion import fetch_all

def fetch_all():
    page = 1
    all_data = []

    while True:
        res = requests.get(f"http://mock-server:5000/api/customers?page={page}&limit=10")
        data = res.json()

        all_data.extend(data["data"])

        if len(data["data"]) < 10:
            break

        page += 1

    return all_data


app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/test-fetch")
def test_fetch():
    data = fetch_all()
    return {"count": len(data)}