"""Pharmacy Claims routes."""
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.core.data_loader import PHARMACY_CLAIMS_DATA, get_record_by_id

router = APIRouter(prefix="/pharmacy-claims", tags=["Pharmacy Claims"])


class PharmacyClaim(BaseModel):
    """Pharmacy Claim schema."""
    rx_claim_id: str
    member_id: str
    patient_name: str
    gender: str
    age: int
    date_filled: str
    drug_name: str
    brand_name: str
    dosage: str
    frequency: str
    days_supply: int
    quantity_dispensed: int
    ndc_code: str
    condition_treated: str
    refill_number: int
    refills_remaining: int
    prescribing_provider: str
    pharmacy_name: str
    copay_amount: str
    plan_paid_amount: str
    fill_status: str


@router.get("", response_model=List[PharmacyClaim], status_code=status.HTTP_200_OK)
async def get_pharmacy_claims() -> List[PharmacyClaim]:
    """
    Get all pharmacy claims.
    
    Returns:
        List[PharmacyClaim]: List of pharmacy claims
    """
    return PHARMACY_CLAIMS_DATA


@router.get("/{rx_claim_id}", response_model=PharmacyClaim, status_code=status.HTTP_200_OK)
async def get_pharmacy_claim(rx_claim_id: str) -> PharmacyClaim:
    """
    Get a specific pharmacy claim by ID.
    
    Args:
        rx_claim_id: Prescription claim ID
        
    Returns:
        PharmacyClaim: Pharmacy claim details
    """
    record = get_record_by_id(PHARMACY_CLAIMS_DATA, "rx_claim_id", rx_claim_id)
    if not record:
        raise HTTPException(status_code=404, detail="Pharmacy claim not found")
    return record
