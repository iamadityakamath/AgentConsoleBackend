"""Health check endpoint."""
from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
from app.core.config import get_settings


router = APIRouter(tags=["Health"])


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    message: str
    timestamp: datetime
    app_name: str
    app_version: str
    environment: str


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API is running and healthy"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Health status of the API
    """
    settings = get_settings()
    
    return HealthResponse(
        status="healthy",
        message="API is running",
        timestamp=datetime.utcnow(),
        app_name=settings.APP_NAME,
        app_version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT
    )
