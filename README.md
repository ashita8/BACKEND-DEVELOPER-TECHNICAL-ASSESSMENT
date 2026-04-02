## Overview
This project implements a data pipeline using:
- Flask (mock API)
- FastAPI (data ingestion)
- PostgreSQL (database)

Flow:
Flask → FastAPI → PostgreSQL → API response

## Prerequisites
- Docker
- Docker Compose
- Python 3.10+

## Run the project

docker-compose up -d

## API Endpoints

### Flask (Mock Server)
GET /api/customers?page=1&limit=5
GET /api/customers/{id}
GET /api/health

### FastAPI (Pipeline)

POST /api/ingest  
→ Fetches data from Flask and stores in DB

GET /api/customers?page=1&limit=5  
→ Returns paginated customers

GET /api/customers/{id}  
→ Returns single customer

## Testing

# Flask
curl "http://localhost:5000/api/customers?page=1&limit=5"

# Ingest data
curl -X POST http://localhost:8000/api/ingest

# Fetch from DB
curl "http://localhost:8000/api/customers?page=1&limit=5"

project-root/
├── docker-compose.yml        # Orchestrates all services
├── README.md                 # Project documentation

├── mock-server/              # Flask mock API
│   ├── app.py                # Flask application (API endpoints)
│   ├── Dockerfile            # Docker config for Flask service
│   ├── requirements.txt      # Flask dependencies
│   └── data/
│       └── customers.json    # Mock customer dataset

├── pipeline-service/         # FastAPI ingestion service
│   ├── main.py               # FastAPI app (routes & endpoints)
│   ├── database.py           # Database connection setup
│   ├── Dockerfile            # Docker config for FastAPI service
│   ├── requirements.txt      # FastAPI dependencies
│
│   ├── models/               # Database models
│   │   └── customer.py       # Customer table schema
│
│   └── services/             # Business logic layer
│       └── ingestion.py      # Data fetching + upsert logic

## Design Decisions

- Used pagination for scalability
- Implemented upsert to avoid duplicate records
- Separated business logic into services layer