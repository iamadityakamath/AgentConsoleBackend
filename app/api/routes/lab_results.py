"""Lab Results routes."""
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.data_loader import load_lab_results, get_records_by_id

router = APIRouter(prefix="/lab-results", tags=["Lab Results"])


class LabResult(BaseModel):
    """Lab Result schema."""
    lab_id: str
    member_id: str
    patient_name: str
    gender: str
    age: int
    draw_date: str
    lab_type: str
    test_name: str
    result_value: str | float
    unit: str
    reference_range: str
    result_flag: Optional[str] = None
    ordering_provider: str
    lab_facility: str
    status: str
    clinical_note: Optional[str] = None


@router.get("", response_model=List[LabResult], status_code=status.HTTP_200_OK)
async def get_lab_results() -> List[LabResult]:
    """
    Get all lab results.
    
    Returns:
        List[LabResult]: List of lab results
    """
    return load_lab_results()


@router.get("/{member_id}", response_model=List[LabResult], status_code=status.HTTP_200_OK)
async def get_lab_result(member_id: str) -> List[LabResult]:
    """
    Get all lab results by member ID.
    
    Args:
        member_id: Member ID
        
    Returns:
        List[LabResult]: Lab result details
    """
    records = get_records_by_id(load_lab_results(), "member_id", member_id)
    if not records:
        raise HTTPException(status_code=404, detail="Lab result not found for this member")
    return records
