"""Care Gap Reports routes."""
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.data_loader import load_care_gaps, get_records_by_id

router = APIRouter(prefix="/care-gaps", tags=["Care Gaps"])


class CareGapReport(BaseModel):
    """Care Gap Report schema."""
    gap_id: str
    member_id: str
    patient_name: str
    gender: str
    age: int
    gap_category: str
    gap_description: str
    clinical_guideline: str
    last_completed_date: Optional[str] = None
    days_overdue: int
    priority: str
    recommended_action: str
    gap_status: str
    assigned_to: str
    gap_notes: Optional[str] = None


@router.get("", response_model=List[CareGapReport], status_code=status.HTTP_200_OK)
async def get_care_gaps() -> List[CareGapReport]:
    """
    Get all care gap reports.
    
    Returns:
        List[CareGapReport]: List of care gap reports
    """
    return load_care_gaps()


@router.get("/{member_id}", response_model=List[CareGapReport], status_code=status.HTTP_200_OK)
async def get_care_gap(member_id: str) -> List[CareGapReport]:
    """
    Get all care gap reports by member ID.
    
    Args:
        member_id: Member ID
        
    Returns:
        List[CareGapReport]: Care gap report details
    """
    records = get_records_by_id(load_care_gaps(), "member_id", member_id)
    if not records:
        raise HTTPException(status_code=404, detail="Care gap not found for this member")
    return records
