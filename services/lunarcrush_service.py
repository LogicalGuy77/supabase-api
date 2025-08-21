from config import get_supabase_client
from models import LunarCrushDataModel, PaginatedResponse
from typing import List, Dict, Any
import math

class LunarCrushService:
    def __init__(self):
        self.supabase = get_supabase_client()
        self.table_name = "lunarcrush_data"

    async def get_total_count(self) -> int:
        """
        Get the total count of records by calling a dedicated database function.
        """
        try:
            # Try RPC call first
            response = self.supabase.rpc('get_lunarcrush_count').execute()
            return response.data if response.data else 0
        except Exception as e:
            print(f"Error getting total count via RPC: {e}")
            # Fallback to direct count query
            try:
                response = self.supabase.table(self.table_name).select("db_id", count="exact").execute()
                return response.count if response.count else 0
            except Exception as fallback_error:
                print(f"Fallback count query also failed: {fallback_error}")
                return 0

    async def get_paginated_data(
        self, 
        page: int = 1, 
        page_size: int = 100,
        coin_name: str = None,
        creator_name: str = None,
        post_type: str = None
    ) -> PaginatedResponse:
        """
        Get paginated data from lunarcrush_data table
        
        Args:
            page: Page number (1-based)
            page_size: Number of records per page (max 1000)
            coin_name: Optional filter by coin name
            creator_name: Optional filter by creator name
            post_type: Optional filter by post type
        """
        # Validate and limit page_size
        page_size = min(max(1, page_size), 1000)  # Limit to max 1000 records per page
        page = max(1, page)  # Ensure page is at least 1
        
        # Calculate offset
        offset = (page - 1) * page_size
        
        try:
            # Build query
            query = self.supabase.table(self.table_name).select("*")
            
            # Apply filters if provided
            if coin_name:
                query = query.ilike("coin_name", f"%{coin_name}%")
            if creator_name:
                query = query.ilike("creator_name", f"%{creator_name}%")
            if post_type:
                query = query.eq("post_type", post_type)
            
            # Get total count for filtered queries
            if coin_name or creator_name or post_type:
                count_query = self.supabase.table(self.table_name).select("db_id", count="exact")
                if coin_name:
                    count_query = count_query.ilike("coin_name", f"%{coin_name}%")
                if creator_name:
                    count_query = count_query.ilike("creator_name", f"%{creator_name}%")
                if post_type:
                    count_query = count_query.eq("post_type", post_type)
                
                count_response = count_query.execute()
                total_count = count_response.count if count_response.count else 0
            else:
                # For unfiltered queries, use the direct count
                total_count = await self.get_total_count()
            
            # Apply pagination
            query = query.range(offset, offset + page_size - 1).order("db_id")
            
            # Execute query
            response = query.execute()
            
            # Convert to Pydantic models
            data = [LunarCrushDataModel(**row) for row in response.data]
            
            # Calculate pagination metadata
            total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0
            has_next = page < total_pages
            has_previous = page > 1
            
            return PaginatedResponse(
                data=data,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=has_next,
                has_previous=has_previous
            )
            
        except Exception as e:
            print(f"Error fetching paginated data: {e}")
            return PaginatedResponse(
                data=[],
                total_count=0,
                page=page,
                page_size=page_size,
                total_pages=0,
                has_next=False,
                has_previous=False
            )

    async def get_by_id(self, db_id: int) -> LunarCrushDataModel:
        """Get a specific record by db_id"""
        try:
            response = self.supabase.table(self.table_name).select("*").eq("db_id", db_id).execute()
            if response.data:
                return LunarCrushDataModel(**response.data[0])
            return None
        except Exception as e:
            print(f"Error fetching record by ID: {e}")
            return None

    async def get_unique_coins(self) -> List[str]:
        """
        Get a list of all unique coin names from the database.
        """
        try:
            # First try the RPC function
            response = self.supabase.rpc('get_unique_coin_names').execute()
            print(f"RPC Response Data: {response.data}")
            
            if response.data:
                if isinstance(response.data, list):
                    coin_names = []
                    for item in response.data:
                        if isinstance(item, dict) and 'coin_name' in item:
                            coin_names.append(item['coin_name'])
                    print(f"Extracted coin names: {coin_names}")
                    return coin_names
                return []
            return []
        except Exception as e:
            print(f"Error fetching unique coins via RPC: {e}")
            
            # Fallback: Use PostgREST's built-in aggregation to get ALL unique values
            try:
                print("Falling back to PostgREST aggregation...")
                
                # Use Supabase's select distinct functionality
                # This should be more efficient than our RPC function
                response = self.supabase.from_(self.table_name).select("coin_name").not_.is_("coin_name", "null").execute()
                
                if response.data:
                    # Extract unique values from all the data
                    all_coin_names = [row["coin_name"] for row in response.data if row.get("coin_name")]
                    unique_coins = sorted(list(set(all_coin_names)))
                    print(f"Found {len(unique_coins)} unique coins from {len(all_coin_names)} total records")
                    return unique_coins
                return []
                
            except Exception as fallback_error:
                print(f"PostgREST aggregation failed: {fallback_error}")
                
                # Final fallback: Paginated approach to get ALL data in chunks
                try:
                    print("Using paginated approach to process ALL data...")
                    all_coins = set()
                    page_size = 1000
                    offset = 0
                    
                    while True:
                        chunk_response = self.supabase.table(self.table_name).select("coin_name").range(offset, offset + page_size - 1).execute()
                        
                        if not chunk_response.data or len(chunk_response.data) == 0:
                            break
                            
                        # Process this chunk
                        chunk_coins = set([row["coin_name"] for row in chunk_response.data if row.get("coin_name")])
                        all_coins.update(chunk_coins)
                        
                        print(f"Processed {offset + len(chunk_response.data)} records, found {len(all_coins)} unique coins so far...")
                        
                        # If we got less than page_size, we've reached the end
                        if len(chunk_response.data) < page_size:
                            break
                            
                        offset += page_size
                        
                        # Safety break to avoid infinite loops
                        if offset > 500000:  # Adjust this limit as needed
                            print("Reached safety limit, stopping pagination")
                            break
                    
                    final_coins = sorted(list(all_coins))
                    print(f"Final result: {len(final_coins)} unique coins from ALL data")
                    return final_coins
                    
                except Exception as final_error:
                    print(f"Paginated approach also failed: {final_error}")
                    return []

    async def get_statistics(self) -> Dict[str, Any]:
        """Get basic statistics about the data"""
        try:
            total_count = await self.get_total_count()
            unique_coins = await self.get_unique_coins()
            
            return {
                "total_records": total_count,
                "unique_coins_count": len(unique_coins),
                "sample_coins": unique_coins[:10] if unique_coins else []
            }
        except Exception as e:
            print(f"Error fetching statistics: {e}")
            return {
                "total_records": 0,
                "unique_coins_count": 0,
                "sample_coins": []
            }
