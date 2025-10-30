"""Debug script to start app and see all errors"""
import sys
import io

# Fix Windows encoding first
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("=" * 60)
print("STARTING GYM RAG APP (DEBUG MODE)")
print("=" * 60)

try:
    print("\n[1/5] Importing FastAPI...")
    from fastapi import FastAPI
    print("[OK] FastAPI imported")
    
    print("\n[2/5] Importing app module...")
    import app as gym_app
    print("[OK] App module imported")
    
    print("\n[3/5] Importing uvicorn...")
    import uvicorn
    print("[OK] Uvicorn imported")
    
    print("\n[4/5] Starting server...")
    print("Server will start on: http://0.0.0.0:8000")
    print("Open browser: http://localhost:8000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    print("\n[5/5] Running app...")
    uvicorn.run(gym_app.app, host="0.0.0.0", port=8000, log_level="info")
    
except KeyboardInterrupt:
    print("\n\n[STOPPED] Server stopped by user")
except Exception as e:
    print(f"\n\n[ERROR] Failed to start app!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

