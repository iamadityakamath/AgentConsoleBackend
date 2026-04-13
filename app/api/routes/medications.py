"""Medications routes."""
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.data_loader import load_medications, get_records_by_id

router = APIRouter(prefix="/medications", tags=["Medications"])


class Medication(BaseModel):
    """Medication schema."""
    med_id: str
    member_id: str
    patient_name: str
    gender: str
    age: int
    drug_name: str
    brand_name: str
    dosage: Optional[str] = None
    route: str
    frequency: str
    indication: str
    prescribing_provider: str
    date_prescribed: str
    last_fill_date: Optional[str] = None
    days_since_last_fill: int
    adherence_status: str
    medication_status: str
    rx_notes: Optional[str] = None


@router.get("", response_model=List[Medication], status_code=status.HTTP_200_OK)
async def get_medications() -> List[Medication]:
    """
    Get all medications.
    
    Returns:
        List[Medication]: List of medications
    """
    return load_medications()


@router.get("/{member_id}", response_model=List[Medication], status_code=status.HTTP_200_OK)
async def get_medication(member_id: str) -> List[Medication]:
    """
    Get all medications by member ID.
    
    Args:
        member_id: Member ID
        
    Returns:
        List[Medication]: Medication details
    """
    records = get_records_by_id(load_medications(), "member_id", member_id)
    if not records:
        raise HTTPException(status_code=404, detail="Medication not found for this member")
    return records
