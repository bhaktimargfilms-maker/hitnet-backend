from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import json, os

app = FastAPI(title="Hitnet.in Search API")

# data.json ফাইলের সঠিক পথ নির্ধারণ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.json")

class Result(BaseModel):
    url: str
    snippet: str

@app.get("/")
def home():
    return {"message": "Welcome to Hitnet.in Search API 🚀", "example": "/search?q=krishna"}

@app.get("/search", response_model=List[Result])
def search(q: str = Query(..., min_length=1)):
    # ফাইল আছে কিনা চেক করা
    if not os.path.exists(DATA_FILE):
        return [{"url": "#", "snippet": "Error: data.json not found on server."}]

    # data.json পড়া
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [{"url": "#", "snippet": f"Error reading data.json: {e}"}]

    q_lower = q.lower()
    results = []

    # সার্চ কুয়েরির সাথে ম্যাচ করা
    for item in data:
        if q_lower in item["text"].lower():
            results.append({
                "url": item["url"],
                "snippet": item["text"][:300] + "..."
            })

    if not results:
        results = [{"url": "#", "snippet": f"No results found for '{q}'"}]

    return results
