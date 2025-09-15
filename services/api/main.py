from fastapi import FastAPI
from services.shared.telemetry import setup_tracing
from services.shared.cosmos import ensure_containers
from services.api.routers import health, demo

app = FastAPI(title="AI Security Auditor API")

@app.on_event("startup")
def startup():
    setup_tracing("ai-security-auditor-api")
    ensure_containers()

app.include_router(health.router)
app.include_router(demo.router)
