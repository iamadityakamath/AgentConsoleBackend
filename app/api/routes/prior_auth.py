"""Prior Authorization routes."""
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.data_loader import PRIOR_AUTHS_DATA, get_records_by_id

router = APIRouter(prefix="/prior-auth", tags=["Prior Authorization"])


class PriorAuth(BaseModel):
    """Prior Authorization schema."""
    auth_id: str
    member_id: str
    patient_name: str
    gender: str
    age: int
    request_date: str
    auth_type: str
    service_requested: str
    requesting_provider: str
    decision: str
    decision_date: Optional[str] = None
    valid_from: Optional[str] = None
    valid_through: Optional[str] = None
    denial_reason: Optional[str] = None
    appeal_status: Optional[str] = None
    auth_notes: Optional[str] = None


@router.get("", response_model=List[PriorAuth], status_code=status.HTTP_200_OK)
async def get_prior_auths() -> List[PriorAuth]:
    """
    Get all prior authorizations.
    
    Returns:
        List[PriorAuth]: List of prior authorizations
    """
    return PRIOR_AUTHS_DATA


@router.get("/{member_id}", response_model=List[PriorAuth], status_code=status.HTTP_200_OK)
async def get_prior_auth(member_id: str) -> List[PriorAuth]:
    """
    Get all prior authorizations by member ID.
    
    Args:
        member_id: Member ID
        
    Returns:
        List[PriorAuth]: Prior authorization details
    """
    records = get_records_by_id(PRIOR_AUTHS_DATA, "member_id", member_id)
    if not records:
        raise HTTPException(status_code=404, detail="Prior authorization not found for this member")
    return records
