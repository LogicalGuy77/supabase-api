import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://gcuiiaigitjjfrmqemza.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdjdWlpYWlnaXRqamZybXFlbXphIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg5MjA3MTUsImV4cCI6MjA2NDQ5NjcxNX0.sIxSTILBcPzmsMSUVEAQrRSVLnU2UIeZxGyP78adSXI")

def get_supabase_client() -> Client:
    """
    Create and return a Supabase client instance
    """
    return create_client(SUPABASE_URL, SUPABASE_KEY)
