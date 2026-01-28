from fastapi import APIRouter
from services.risk_engine import compute_risk

router = APIRouter()

@router.post("/metrics")
def risk_metrics(payload: dict):
    prices = payload.get("prices", [])
    return compute_risk(prices)
