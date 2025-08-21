from models import LunarCrushDataModel, PaginatedResponse

sample = LunarCrushDataModel(db_id=1)
resp = PaginatedResponse(data=[sample], total_count=1, page=1, page_size=1, total_pages=1, has_next=False, has_previous=False)
print(resp.model_dump())
