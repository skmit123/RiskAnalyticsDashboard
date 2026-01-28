from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.market import router as market_router
from routers.risk import router as risk_router

app = FastAPI(title="Risk Analytics API")

# ---- CORS SETTINGS ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- ROUTERS ----
app.include_router(market_router, prefix="/market")
app.include_router(risk_router, prefix="/risk")

# ---- ROOT ROUTE ----
@app.get("/")
def root():
    return {"message": "Risk Analytics API Running"}

