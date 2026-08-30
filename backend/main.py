"""
main.py - the smallest possible backend, just to prove everyone's setup works.

WHAT THIS FILE DOES:
- Starts a tiny web server using FastAPI
- When someone visits it in a browser, it replies with a friendly message
- This is NOT the real app yet - it's just a "does my computer work?" test

HOW TO RUN THIS (see the Day 1 guide for the full walkthrough):
    pip install -r requirements.txt
    uvicorn main:app --reload

Then open http://127.0.0.1:8000 in your browser.
"""

from fastapi import FastAPI

app = FastAPI(title="PS92 Scheme Navigator - Hello World")


@app.get("/")
def read_root():
    """This runs when someone visits the homepage (the '/' address)."""
    return {"message": "Hello World! The PS92 backend is alive."}


@app.get("/health")
def health_check():
    """A simple check used later to confirm the backend is running correctly."""
    return {"status": "ok"}