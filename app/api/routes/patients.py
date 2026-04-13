"""Patient Demographics routes."""
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.data_loader import PATIENTS_DATA, get_record_by_id

router = APIRouter(prefix="/patients", tags=["Patient Demographics"])


class PatientDemographics(BaseModel):
    """Patient Demographics schema."""
    member_id: str
    full_name: str
    gender: str
    age: int
    date_of_birth: str
    street_address: str
    city: str
    state: str
    zip_code: str | int
    location: str
    phone_primary: str
    phone_secondary: Optional[str] = None
    email_address: Optional[str] = None
    preferred_contact_method: str
    preferred_language: str
    marital_status: str
    employment_status: str
    caregiver_support: Optional[str] = None
    primary_conditions: str
    insurance_plan_type: str
    insurance_start_date: str
    risk_tier: str
    assigned_coordinator: str


@router.get("", response_model=List[PatientDemographics], status_code=status.HTTP_200_OK)
async def get_patients() -> List[PatientDemographics]:
    """
    Get all patient demographics.
    
    Returns:
        List[PatientDemographics]: List of patient demographics
    """
    return PATIENTS_DATA


@router.get("/{member_id}", response_model=PatientDemographics, status_code=status.HTTP_200_OK)
async def get_patient(member_id: str) -> PatientDemographics:
    """
    Get a specific patient by member ID.
    
    Args:
        member_id: Member ID
        
    Returns:
        PatientDemographics: Patient demographics details
    """
    record = get_record_by_id(PATIENTS_DATA, "member_id", member_id)
    if not record:
        raise HTTPException(status_code=404, detail="Patient not found")
    return record
