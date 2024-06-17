from http.client import HTTPException

import pytest
import requests
import requests_mock

from config import settings
from services.xero_service import XeroService
from tests.test_reponse import sample_response


@pytest.fixture
def xero_service():
    return XeroService(base_url=settings.xero_api_base_url)


@pytest.fixture
def requests_mock_fixture():
    with requests_mock.Mocker() as m:
        yield m


def test_get_balance_sheet_success(xero_service, requests_mock_fixture):
    url = "http://localhost:3000/api.xro/2.0/Reports/BalanceSheet"
    requests_mock_fixture.get(url, json=sample_response, status_code=200)

    response = xero_service.get_balance_sheet()

    assert response.Status == "OK"
    assert len(response.Reports) == 1
    assert response.Reports[0].ReportID == "BalanceSheet"
    assert response.Reports[0].ReportName == "Balance Sheet"
    assert response.Reports[0].ReportDate == "12 June 2024"

    # Add more assertions as needed to validate the structure and content of the response


def test_get_balance_sheet_timeout(xero_service, requests_mock_fixture):
    url = "http://localhost:3000/api.xro/2.0/Reports/BalanceSheet"
    requests_mock_fixture.get(url, exc=requests.exceptions.Timeout)

    with pytest.raises(HTTPException) as excinfo:
        xero_service.get_balance_sheet()

    assert excinfo.value.status_code == 504
    assert "timed out" in excinfo.value.detail


def test_get_balance_sheet_request_exception(xero_service, requests_mock_fixture):
    url = "http://localhost:3000/api.xro/2.0/Reports/BalanceSheet"
    requests_mock_fixture.get(url, status_code=500)

    with pytest.raises(HTTPException) as excinfo:
        xero_service.get_balance_sheet()

    assert excinfo.value.status_code == 500
    assert "Failed to connect" in excinfo.value.detail


def test_get_balance_sheet_invalid_response(xero_service, requests_mock_fixture):
    url = "http://localhost:3000/api.xro/2.0/Reports/BalanceSheet"
    requests_mock_fixture.get(url, text="Invalid JSON")

    with pytest.raises(HTTPException) as excinfo:
        xero_service.get_balance_sheet()

    assert excinfo.value.status_code == 500
    assert "invalid response" in excinfo.value.detail
