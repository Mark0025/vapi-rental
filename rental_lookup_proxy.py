import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from main import extract_rentals_from_website

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RentalLookupRequest(BaseModel):
    website: str

@app.post("/rental-lookup")
async def rental_lookup(payload: RentalLookupRequest):
    if not payload.website:
        raise HTTPException(status_code=400, detail="Missing website parameter")
    try:
        result = extract_rentals_from_website(payload.website)
        return result
    except Exception as e:
        print(f"Proxy error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# To run: uv run -m uvicorn rental_lookup_proxy:app --host 0.0.0.0 --port 4242 