from fastapi import FastAPI ,Query, HTTPException
from database import engine,SessionLocal
from models.customer import Base ,Customer
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

@app.get("/api/customers")
def get_customers(page: int = Query(1), limit: int = Query(10)):
    db = SessionLocal()

    offset = (page - 1) * limit
    customers = db.query(Customer).offset(offset).limit(limit).all()

    total = db.query(Customer).count()

    result = [c.__dict__ for c in customers]

    # remove SQLAlchemy internal key
    for r in result:
        r.pop("_sa_instance_state", None)

    db.close()

    return {
        "data": result,
        "total": total,
        "page": page,
        "limit": limit
    }

@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: str):
    db = SessionLocal()

    customer = db.query(Customer).filter_by(customer_id=customer_id).first()

    if not customer:
        db.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    result = customer.__dict__
    result.pop("_sa_instance_state", None)

    db.close()

    return result