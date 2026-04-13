"""EHR Clinical Notes routes."""
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.data_loader import load_ehr_notes, get_records_by_id

router = APIRouter(prefix="/ehr-notes", tags=["EHR Clinical Notes"])


class EHRClinicalNote(BaseModel):
    """EHR Clinical Note schema."""
    note_id: str
    member_id: str
    patient_name: str
    gender: str
    age: int
    location: str
    note_date: str
    note_type: str
    provider_name: str
    facility_name: str
    icd_code: str
    primary_diagnosis: str
    subjective: str
    objective: str
    assessment: str
    plan: str
    follow_up_date: Optional[str] = None


@router.get("", response_model=List[EHRClinicalNote], status_code=status.HTTP_200_OK)
async def get_ehr_notes() -> List[EHRClinicalNote]:
    """
    Get all EHR clinical notes.
    
    Returns:
        List[EHRClinicalNote]: List of clinical notes
    """
    return load_ehr_notes()


@router.get("/{member_id}", response_model=List[EHRClinicalNote], status_code=status.HTTP_200_OK)
async def get_ehr_note(member_id: str) -> List[EHRClinicalNote]:
    """
    Get all EHR clinical notes by member ID.
    
    Args:
        member_id: Member ID
        
    Returns:
        List[EHRClinicalNote]: Clinical note details
    """
    records = get_records_by_id(load_ehr_notes(), "member_id", member_id)
    if not records:
        raise HTTPException(status_code=404, detail="Clinical note not found for this member")
    return records
