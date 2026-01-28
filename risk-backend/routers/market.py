from fastapi import APIRouter
from services.data_fetcher import get_market_data

router = APIRouter()

@router.get("/{ticker}")
def fetch_market_data(ticker: str):
    return get_market_data(ticker.upper())
