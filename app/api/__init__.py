"""API routes module."""
import logging
from importlib import import_module

from fastapi import APIRouter
from app.core.constants import API_V1_PREFIX


logger = logging.getLogger(__name__)


# Create main router for v1 API
api_v1_router = APIRouter(prefix=API_V1_PREFIX)

def _include_router(module_path: str, required: bool = False) -> None:
    """Import a router module and include it, optionally failing hard if required."""

    try:
        module = import_module(module_path)
        api_v1_router.include_router(module.router)
    except Exception:
        if required:
            raise
        logger.exception("Skipping router due to import failure: %s", module_path)


# Health route is required.
_include_router("app.api.routes.health", required=True)

# All non-health routes are optional in serverless startup.
_include_router("app.api.routes.ai_routes.undertand_patient_data")
_include_router("app.api.routes.ai_routes.frame_questions")

_include_router("app.api.routes.care_gaps")
_include_router("app.api.routes.ehr_notes")
_include_router("app.api.routes.insurance_claims")
_include_router("app.api.routes.lab_results")
_include_router("app.api.routes.medications")
_include_router("app.api.routes.patients")
_include_router("app.api.routes.pharmacy_claims")
_include_router("app.api.routes.prior_auth")
