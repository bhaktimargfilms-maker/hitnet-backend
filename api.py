from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import json, os

app = FastAPI(title="Hitnet.in Search API")

# ফাইলের লোকেশন (api.py এর পাশেই data.json থাকবে)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

class Result(BaseModel):
    url: str
    snippet: str

@app.get("/")
def home():
    return {
        "message": "Welcome to Hitnet.in Search API 🚀",
        "example": "/search?q=krishna"
    }

@app.get("/search", response_model=List[Result])
def search(q: str = Query(..., min_length=1)):
    # data.json আছে কিনা চেক
    if not os.path.exists(DATA_FILE):
        return [{"url": "#", "snippet": "Error: data.json not found on server."}]

    # ফাইল পড়া
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [{"url": "#", "snippet": f"Error reading data.json: {e}"}]

    q_lower = q.lower()
    results = []

    # সার্চ করা
    for item in data:
        if q_lower in item["snippet"].lower():
            results.append({
                "url": item["url"],
                "snippet": item["snippet"]
            })

    if not results:
        results = [{"url": "#", "snippet": f"No results found for '{q}'"}]

    return results
