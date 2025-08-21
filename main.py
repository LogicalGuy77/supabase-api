from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.lunarcrush_service import LunarCrushService
from models import PaginatedResponse
from typing import Optional

# Create FastAPI instance
app = FastAPI(
    title="LunarCrush Data API",
    description="A production-ready API to serve LunarCrush data from Supabase.",
    version="2.0.0"
)

# CORS Middleware for production readiness
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Initialize service
lunarcrush_service = LunarCrushService()

@app.get("/data", response_model=PaginatedResponse)
async def get_lunarcrush_data(
    page: int = Query(1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(100, ge=1, le=1000, description="Number of records per page (max 1000)"),
    coin_name: Optional[str] = Query(None, description="Filter by coin name (case-insensitive partial match)"),
    creator_name: Optional[str] = Query(None, description="Filter by creator name (case-insensitive partial match)"),
    post_type: Optional[str] = Query(None, description="Filter by post type (exact match)")
):
    """
    Get paginated LunarCrush data with optional filters.
    
    - **page**: Page number (starts from 1)
    - **page_size**: Number of records per page (1-1000)
    - **coin_name**: Optional filter by coin name
    - **creator_name**: Optional filter by creator name
    - **post_type**: Optional filter by post type
    """
    try:
        result = await lunarcrush_service.get_paginated_data(
            page=page,
            page_size=page_size,
            coin_name=coin_name,
            creator_name=creator_name,
            post_type=post_type
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data: {str(e)}")

@app.get("/statistics")
async def get_statistics():
    """
    Get basic statistics about the LunarCrush data, including total record count
    and a list of all unique coin names.
    """
    try:
        stats = await lunarcrush_service.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
