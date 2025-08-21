# LunarCrush Supabase API

Production-ready FastAPI service exposing LunarCrush data stored in Supabase with pagination & statistics endpoints.

## Setup

1. Uses Python 3.13 (FastAPI 0.112.x + Pydantic v2 stack).

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /data` - Paginated dataset with optional filters (coin_name, creator_name, post_type)
- `GET /statistics` - Basic statistics (total records, unique coins sample)
- `GET /health` - Health check

## Documentation

Once the server is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
