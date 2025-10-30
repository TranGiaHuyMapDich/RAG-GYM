"""Simple test to see where app crashes"""
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("Step 1: Import FastAPI...")
from fastapi import FastAPI
print("OK")

print("Step 2: Import RAG system...")
from rag_system_simple import GymRAGSystem
print("OK")

print("Step 3: Create RAG instance...")
rag = GymRAGSystem("megaGymDataset.csv")
print("OK")

print("Step 4: Initialize vector store...")
try:
    rag.initialize_vector_store(force_recreate=False)
    print("OK - Vector store initialized")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

print("Step 5: Import Supabase...")
try:
    from supabase_client import get_supabase_manager
    sb = get_supabase_manager()
    print("OK - Supabase connected")
except Exception as e:
    print(f"WARNING: Supabase not available: {e}")

print("\nAll tests passed! Starting server...")

print("Step 6: Create FastAPI app...")
app = FastAPI()
print("OK")

print("Step 7: Start uvicorn...")
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)

