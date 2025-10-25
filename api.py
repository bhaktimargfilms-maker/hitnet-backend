from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import json, os

app = FastAPI(title="Hitnet.in Search API")

DATA_FILE = os.path.join("indexdir", "data.json")

class Result(BaseModel):
    url: str
    snippet: str

@app.get("/search", response_model=List[Result])
def search(q: str = Query(..., min_length=1)):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    q_lower = q.lower()
    results = []
    for item in data:
        if q_lower in item["text"].lower():
            results.append({
                "url": item["url"],
                "snippet": item["text"][:300] + "..."
            })
    return results
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import json, os

app = FastAPI(title="Hitnet.in Search API")

# Safe path (works on Render)
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
    # Ensure file exists
    if not os.path.exists(DATA_FILE):
        return [{"url": "#", "snippet": "data.json file not found on server"}]

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return [{"url": "#", "snippet": f"Error reading data.json: {e}"}]

    q_lower = q.lower()
    results = [
        {"url": item["url"], "snippet": item["snippet"]}
        for item in data if q_lower in item["snippet"].lower()
    ]

    if not results:
        return [{"url": "#", "snippet": f"No results found for '{q}'"}]

    return results
