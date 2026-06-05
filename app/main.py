from fastapi import FastAPI

from app.api.v1.endpoints.student import router as student_router
from app.api.v1.endpoints.analytics import router as analytics_router
from app.api.v1.endpoints.reports import router as report_router
from app.api.v1.endpoints.health import router as health_router

app = FastAPI(
    title="Student Analytics ERP",
    description=(
        "Advanced Student Management System with analytics, risk scoring, "
        "engagement tracking, performance classification, and report generation."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── API v1 routers ────────────────────────────────────────────────────────────
API_PREFIX = "/api/v1"

app.include_router(student_router, prefix=API_PREFIX)
app.include_router(analytics_router, prefix=API_PREFIX)
app.include_router(report_router, prefix=API_PREFIX)
app.include_router(health_router, prefix=f"{API_PREFIX}/health", tags=["Health"])


# ── Root & legacy health endpoints ────────────────────────────────────────────
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Student Analytics ERP API is running",
        "docs": "/docs",
        "version": "1.0.0",
    }