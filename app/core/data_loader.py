"""
Data loader for reading Excel files from Data folder.

This module loads all Excel files from the Data folder and provides
cached access to the data.
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from functools import lru_cache


# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_FOLDER = PROJECT_ROOT / "Data"


def _normalize_value(value: Any) -> Any:
    """Convert pandas/numpy values into JSON-safe Python types."""
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return value.item()
        except Exception:
            return value
    return value


def _read_excel_records(file_path: Path) -> List[Dict[str, Any]]:
    """Read one Excel file and return normalized records."""
    df = pd.read_excel(file_path)
    records = df.to_dict(orient="records")
    return [
        {key: _normalize_value(value) for key, value in record.items()}
        for record in records
    ]


@lru_cache(maxsize=1)
def load_care_gaps() -> List[Dict[str, Any]]:
    """
    Load care gap reports from Excel file.
    
    Returns:
        List[Dict[str, Any]]: List of care gap records
    """
    try:
        file_path = DATA_FOLDER / "care_gap_reports_mock.xlsx"
        if not file_path.exists():
            return []
        
        return _read_excel_records(file_path)
    except Exception as e:
        print(f"Error loading care_gaps: {e}")
        return []


@lru_cache(maxsize=1)
def load_ehr_notes() -> List[Dict[str, Any]]:
    """
    Load EHR clinical notes from Excel file.
    
    Returns:
        List[Dict[str, Any]]: List of EHR note records
    """
    try:
        file_path = DATA_FOLDER / "ehr_clinical_notes_mock.xlsx"
        if not file_path.exists():
            return []
        
        return _read_excel_records(file_path)
    except Exception as e:
        print(f"Error loading ehr_notes: {e}")
        return []


@lru_cache(maxsize=1)
def load_insurance_claims() -> List[Dict[str, Any]]:
    """
    Load insurance claims from Excel file.
    
    Returns:
        List[Dict[str, Any]]: List of insurance claim records
    """
    try:
        file_path = DATA_FOLDER / "insurance_claims_mock.xlsx"
        if not file_path.exists():
            return []
        
        return _read_excel_records(file_path)
    except Exception as e:
        print(f"Error loading insurance_claims: {e}")
        return []


@lru_cache(maxsize=1)
def load_lab_results() -> List[Dict[str, Any]]:
    """
    Load lab results from Excel file.
    
    Returns:
        List[Dict[str, Any]]: List of lab result records
    """
    try:
        file_path = DATA_FOLDER / "lab_results_mock.xlsx"
        if not file_path.exists():
            return []
        
        return _read_excel_records(file_path)
    except Exception as e:
        print(f"Error loading lab_results: {e}")
        return []


@lru_cache(maxsize=1)
def load_medications() -> List[Dict[str, Any]]:
    """
    Load medications from Excel file.
    
    Returns:
        List[Dict[str, Any]]: List of medication records
    """
    try:
        file_path = DATA_FOLDER / "medication_list_mock.xlsx"
        if not file_path.exists():
            return []
        
        return _read_excel_records(file_path)
    except Exception as e:
        print(f"Error loading medications: {e}")
        return []


@lru_cache(maxsize=1)
def load_patients() -> List[Dict[str, Any]]:
    """
    Load patient demographics from Excel file.
    
    Returns:
        List[Dict[str, Any]]: List of patient records
    """
    try:
        file_path = DATA_FOLDER / "patient_demographics_mock.xlsx"
        if not file_path.exists():
            return []
        
        return _read_excel_records(file_path)
    except Exception as e:
        print(f"Error loading patients: {e}")
        return []


@lru_cache(maxsize=1)
def load_pharmacy_claims() -> List[Dict[str, Any]]:
    """
    Load pharmacy claims from Excel file.
    
    Returns:
        List[Dict[str, Any]]: List of pharmacy claim records
    """
    try:
        file_path = DATA_FOLDER / "pharmacy_claims_mock.xlsx"
        if not file_path.exists():
            return []
        
        return _read_excel_records(file_path)
    except Exception as e:
        print(f"Error loading pharmacy_claims: {e}")
        return []


@lru_cache(maxsize=1)
def load_prior_auths() -> List[Dict[str, Any]]:
    """
    Load prior authorizations from Excel file.
    
    Returns:
        List[Dict[str, Any]]: List of prior auth records
    """
    try:
        file_path = DATA_FOLDER / "prior_auth_mock.xlsx"
        if not file_path.exists():
            return []
        
        return _read_excel_records(file_path)
    except Exception as e:
        print(f"Error loading prior_auths: {e}")
        return []


# Load all data at module initialization
CARE_GAPS_DATA = load_care_gaps()
EHR_NOTES_DATA = load_ehr_notes()
INSURANCE_CLAIMS_DATA = load_insurance_claims()
LAB_RESULTS_DATA = load_lab_results()
MEDICATIONS_DATA = load_medications()
PATIENTS_DATA = load_patients()
PHARMACY_CLAIMS_DATA = load_pharmacy_claims()
PRIOR_AUTHS_DATA = load_prior_auths()


def get_record_by_id(data: List[Dict[str, Any]], id_field: str, id_value: str) -> Dict[str, Any] | None:
    """
    Get a single record from data by ID field.
    
    Args:
        data: List of records
        id_field: Field name to search by
        id_value: Value to match
        
    Returns:
        Dict[str, Any] | None: The matching record or None
    """
    for record in data:
        # Convert to string for comparison
        if str(record.get(id_field, "")) == str(id_value):
            return record
    return None


def get_records_by_id(data: List[Dict[str, Any]], id_field: str, id_value: str) -> List[Dict[str, Any]]:
    """
    Get all matching records from data by ID field.

    Args:
        data: List of records
        id_field: Field name to search by
        id_value: Value to match

    Returns:
        List[Dict[str, Any]]: All matching records
    """
    return [
        record
        for record in data
        if str(record.get(id_field, "")) == str(id_value)
    ]
