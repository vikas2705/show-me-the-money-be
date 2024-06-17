# main.py
import logging

from fastapi import FastAPI, HTTPException

from services.response import BalanceSheetResponse
from services.xero_service import XeroService
from config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define the origins that should be allowed to make cross-origin requests
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # List of allowed origins
    allow_credentials=True,           # Allow cookies and credentials
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)


xero_service = XeroService(base_url=settings.xero_api_base_url)


@app.get("/api/balance-sheet", response_model=BalanceSheetResponse)
async def get_balance_sheet():
    try:
        return xero_service.get_balance_sheet()
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
