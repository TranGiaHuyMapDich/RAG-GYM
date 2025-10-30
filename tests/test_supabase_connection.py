"""Test Supabase Connection"""
import os
import sys
import io
from dotenv import load_dotenv

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path, override=True)
print(f"\nLoading .env from: {env_path}")

print("=" * 60)
print("TESTING SUPABASE CONNECTION")
print("=" * 60)

# Check if env vars are loaded
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print(f"\nSUPABASE_URL: {supabase_url}")
print(f"SUPABASE_KEY: {supabase_key[:50]}..." if supabase_key else "SUPABASE_KEY not found")

# Try to import and create Supabase client
try:
    from supabase import create_client
    print("\n[OK] Supabase package imported successfully")
    
    # Try to create client
    client = create_client(supabase_url, supabase_key)
    print("[OK] Supabase client created successfully")
    
    # Try a simple query
    response = client.table('users').select("count").execute()
    print(f"[OK] Connection successful! Can query database.")
    print(f"     Users table accessible")
    
    print("\n" + "=" * 60)
    print("SUCCESS! SUPABASE IS CONNECTED!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}")
    print(f"        {str(e)}")
    print("\n" + "=" * 60)
    print("FAILED! SUPABASE CONNECTION ERROR!")
    print("=" * 60)

