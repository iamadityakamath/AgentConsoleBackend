"""Insurance Claims routes."""
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.data_loader import load_insurance_claims, get_record_by_id

router = APIRouter(prefix="/insurance-claims", tags=["Insurance Claims"])


class InsuranceClaim(BaseModel):
    """Insurance Claim schema."""
    claim_id: str
    member_id: str
    patient_name: str
    gender: str
    age: int
    location: str
    date_of_service: str
    claim_type: str
    place_of_service: str
    provider_name: str
    facility_name: str
    icd_code: str
    diagnosis_description: str
    cpt_code: Optional[str | float] = None
    procedure_description: str
    billed_amount: str
    claim_status: str


@router.get("", response_model=List[InsuranceClaim], status_code=status.HTTP_200_OK)
async def get_insurance_claims() -> List[InsuranceClaim]:
    """
    Get all insurance claims.
    
    Returns:
        List[InsuranceClaim]: List of insurance claims
    """
    return load_insurance_claims()


@router.get("/{claim_id}", response_model=InsuranceClaim, status_code=status.HTTP_200_OK)
async def get_insurance_claim(claim_id: str) -> InsuranceClaim:
    """
    Get a specific insurance claim by ID.
    
    Args:
        claim_id: Claim ID
        
    Returns:
        InsuranceClaim: Insurance claim details
    """
    record = get_record_by_id(load_insurance_claims(), "claim_id", claim_id)
    if not record:
        raise HTTPException(status_code=404, detail="Insurance claim not found")
    return record
