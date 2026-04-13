"""API routes module."""
from fastapi import APIRouter
from app.api.routes import (
    health,
    care_gaps,
    ehr_notes,
    insurance_claims,
    lab_results,
    medications,
    patients,
    pharmacy_claims,
    prior_auth,
)
from app.api.routes.ai_routes import frame_questions, undertand_patient_data
from app.core.constants import API_V1_PREFIX


# Create main router for v1 API
api_v1_router = APIRouter(prefix=API_V1_PREFIX)

# Include all routers
api_v1_router.include_router(health.router)
api_v1_router.include_router(care_gaps.router)
api_v1_router.include_router(ehr_notes.router)
api_v1_router.include_router(insurance_claims.router)
api_v1_router.include_router(lab_results.router)
api_v1_router.include_router(medications.router)
api_v1_router.include_router(patients.router)
api_v1_router.include_router(pharmacy_claims.router)
api_v1_router.include_router(prior_auth.router)
api_v1_router.include_router(undertand_patient_data.router)
api_v1_router.include_router(frame_questions.router)
