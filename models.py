from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class LunarCrushDataModel(BaseModel):
    db_id: int
    source_file: Optional[str] = None
    uploaded_at: Optional[datetime] = None
    id: Optional[str] = None
    coin_name: Optional[str] = None
    creator_avatar: Optional[str] = None
    creator_display_name: Optional[str] = None
    creator_followers: Optional[str] = None
    creator_id: Optional[str] = None
    creator_name: Optional[str] = None
    interactions_24h: Optional[str] = None
    interactions_total: Optional[str] = None
    post_created: Optional[str] = None
    post_image: Optional[str] = None
    post_link: Optional[str] = None
    post_sentiment: Optional[str] = None
    post_time_interactions: Optional[str] = None
    post_title: Optional[str] = None
    post_type: Optional[str] = None
    scraped_at: Optional[str] = None
    tags: Optional[str] = None
    taxonomy_tag: Optional[str] = None
    taxonomy_subtag: Optional[str] = None
    sentiment: Optional[str] = None
    classification: Optional[str] = None
    description: Optional[str] = None
    aliases: Optional[str] = None
    weight: Optional[str] = None
    threshold: Optional[str] = None

class PaginatedResponse(BaseModel):
    data: List[LunarCrushDataModel]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
