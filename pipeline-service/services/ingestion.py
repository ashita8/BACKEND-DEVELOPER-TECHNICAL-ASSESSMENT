import requests

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