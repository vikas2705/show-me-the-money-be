# services/xero_service.py
from requests import RequestException, Timeout, get
from pydantic import BaseModel
from fastapi import HTTPException
import logging
from config import settings
from services.response import BalanceSheetResponse
from tests.test_reponse import sample_response


class XeroService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_balance_sheet(self) -> BalanceSheetResponse:
        return sample_response
        url = f"{self.base_url}/api.xro/2.0/Reports/BalanceSheet"
        try:
            response = get(url, timeout=10)
            response.raise_for_status()
            return BalanceSheetResponse(**response.json())
        except Timeout:
            logging.error("Request to Xero API timed out")
            raise HTTPException(status_code=504, detail="The request to the Xero API timed out.")
        except RequestException as e:
            logging.error(f"Request to Xero API failed: {e}")
            raise HTTPException(status_code=response.status_code, detail="Failed to connect to the Xero API.")
        except ValueError as e:
            logging.error(f"Invalid response from Xero API: {e}")
            raise HTTPException(status_code=500, detail="Received an invalid response from the Xero API.")
