import os

from supabase import create_client, Client
from flask import current_app
from app.utils.logger import logger

def create_supabase_client():
    logger.info(f'Creating supabase client for {os.getenv('SUPABASE_URL')}')
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


supabase = create_supabase_client()
response = supabase.table('conversations').select(
    '''SELECT *
     FROM conversations''').execute()

