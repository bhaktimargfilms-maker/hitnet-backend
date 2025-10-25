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

DATA_FILE = "data.json"

class Result(BaseModel):
    url: str
    snippet: str

@app.get("/search", response_model=List[Result])
def search(q: str = Query(..., min_length=1)):
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
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

DATA_FILE = "data.json"  # indexdir/ দরকার নেই

class Result(BaseModel):
    url: str
    snippet: str

@app.get("/search", response_model=List[Result])
def search(q: str = Query(..., min_length=1)):
    # চেক করো data.json ফাইল আছে কিনা
    if not os.path.exists(DATA_FILE):
        return []

    # ডাটা লোড করো
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    q_lower = q.lower()
    results = []

    # কুয়েরির সাথে ম্যাচ করো
    for item in data:
        if q_lower in item["snippet"].lower():
            results.append({
                "url": item["url"],
                "snippet": item["snippet"]
            })

    return results

