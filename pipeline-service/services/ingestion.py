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

    allowed_fields = {
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "address",
        "date_of_birth",
        "account_balance",
        "created_at"
    }

    for c in customers:
        # filter only valid fields
        filtered = {k: v for k, v in c.items() if k in allowed_fields}

        existing = db.query(Customer).filter_by(customer_id=c["customer_id"]).first()

        if existing:
            for key, value in filtered.items():
                setattr(existing, key, value)
        else:
            db.add(Customer(**filtered))

    db.commit()
    db.close()