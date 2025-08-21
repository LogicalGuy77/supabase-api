# FastAPI Supabase Backend

A simple FastAPI backend with a single endpoint.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /query` - Returns "HI"

## Documentation

Once the server is running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc
