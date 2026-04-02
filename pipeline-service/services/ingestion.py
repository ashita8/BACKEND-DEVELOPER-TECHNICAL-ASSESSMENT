import requests
from database import SessionLocal
from models.customer import Customer


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


def upsert_customers(customers):
    db = SessionLocal()

    for c in customers:
        existing = db.query(Customer).filter_by(customer_id=c["customer_id"]).first()

        if existing:
            for key, value in c.items():
                setattr(existing, key, value)
        else:
            db.add(Customer(**c))

    db.commit()
    db.close()