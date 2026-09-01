"""
main.py — the real FastAPI skeleton (Day 2 version).

This replaces the Day 1 "Hello World" file. It now:
- Allows the frontend (running on a different port) to talk to this backend (CORS)
- Includes the /schemes and /channel-partners endpoints
- Keeps a /health check for quick testing

HOW TO RUN:
    pip install -r requirements.txt
    uvicorn main:app --reload

Then visit http://127.0.0.1:8000/schemes in your browser.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import schemes

app = FastAPI(title="PS92 Scheme Navigator")

# Allow the frontend (e.g. opened as a local file, or served on another port)
# to call this backend without the browser blocking the request.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for a hackathon prototype; tighten later if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schemes.router)


@app.get("/")
def read_root():
    return {"message": "PS92 backend is running. Try /schemes or /health."}


@app.get("/health")
def health_check():
    return {"status": "ok"}