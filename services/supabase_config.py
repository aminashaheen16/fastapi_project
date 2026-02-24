from supabase import create_client
from fastapi import HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None

if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL != "your_supabase_url_here":
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("⚠️  Warning: Supabase credentials not configured. Database features will not work.")


def get_supabase():
    """Returns the Supabase client or raises a 503 if not configured."""
    if supabase is None:
        raise HTTPException(
            status_code=503,
            detail="Database not configured. Please set SUPABASE_URL and SUPABASE_KEY in your .env file."
        )
    return supabase