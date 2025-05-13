from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
from typing import List, Optional
import uvicorn
import os
import asyncio
from cachetools import TTLCache

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the frontend directory
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_dir), name="frontend")

@app.get("/")
async def root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

# Cache for storing suggestions (cache for 1 hour)
suggestions_cache = TTLCache(maxsize=1000, ttl=3600)

async def get_datamuse_suggestions(prefix: str) -> List[str]:
    """Get word suggestions from DataMuse API"""
    try:
        async with httpx.AsyncClient() as client:
            # Get words that start with prefix
            response = await client.get(f"https://api.datamuse.com/sug?s={prefix}")
            data = response.json()
            words = [item["word"] for item in data]

            # Also get words that sound like the prefix
            response2 = await client.get(f"https://api.datamuse.com/words?sl={prefix}")
            data2 = response2.json()
            sound_like_words = [item["word"] for item in data2 if item["word"].startswith(prefix)]

            # Combine and remove duplicates while preserving order
            all_words = []
            seen = set()
            for word in words + sound_like_words:
                if word not in seen:
                    all_words.append(word)
                    seen.add(word)

            return all_words[:20]  # Return top 20 suggestions
    except Exception as e:
        print(f"Error fetching from DataMuse API: {e}")
        return []

@app.get("/api/suggestions")
async def suggestions(prefix: str):
    if not prefix or len(prefix) < 2:
        return []
    
    # Check cache first
    cache_key = f"suggestions_{prefix}"
    if cache_key in suggestions_cache:
        return suggestions_cache[cache_key]
    
    # Get suggestions from DataMuse API
    suggestions = await get_datamuse_suggestions(prefix)
    
    # Cache the results
    if suggestions:
        suggestions_cache[cache_key] = suggestions
    
    return suggestions

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=5000, reload=True) 