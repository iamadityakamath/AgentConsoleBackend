# Vedara Agent Console Backend API

FastAPI backend for Vedara Agent Console, including patient-data routes and AI-assisted routes.

## Prerequisites

- Python 3.9+
- `pip`

## Quick Start

### 1) Create and activate virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment

Create `.env` at project root and set at least:

```env
APP_NAME=Vedara Agent Console API
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development
BASE_URL=http://localhost:8000
HOST=0.0.0.0
PORT=8000

LOG_LEVEL=INFO
LOG_FILE=logs/app.log

OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=
API_KEY=

ALLOWED_ORIGINS=["*"]
ALLOWED_CREDENTIALS=false
ALLOWED_METHODS=["*"]
ALLOWED_HEADERS=["*"]
```

Notes:

- `.env` is gitignored. Do not commit secrets.
- `undertand_patient_data` currently calls OpenAI live.

### 4) Run locally

```bash
python main.py
```

API base URL:

```text
http://localhost:8000
```

## API Docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Core Routes

- `GET /api/v1/health`
- `POST /api/v1/ai/undertand_patient_data`
- `POST /api/v1/ai/frame-questions`

## Data Inventory

The `Data` folder currently contains 8 Excel tables:

- `care_gap_reports_mock.xlsx` (110 rows, 15 columns)
- `ehr_clinical_notes_mock.xlsx` (31 rows, 17 columns)
- `insurance_claims_mock.xlsx` (71 rows, 17 columns)
- `lab_results_mock.xlsx` (293 rows, 16 columns)
- `medication_list_mock.xlsx` (108 rows, 18 columns)
- `patient_demographics_mock.xlsx` (30 rows, 23 columns)
- `pharmacy_claims_mock.xlsx` (144 rows, 21 columns)
- `prior_auth_mock.xlsx` (55 rows, 16 columns)

Generated references with per-table columns and sample values:

- `Data/data_dictionary.md`
- `Data/data_dictionary.json`

### Column Names By Table

- `care_gap_reports_mock.xlsx`: gap_id, member_id, patient_name, gender, age, gap_category, gap_description, clinical_guideline, last_completed_date, days_overdue, priority, recommended_action, gap_status, assigned_to, gap_notes
- `ehr_clinical_notes_mock.xlsx`: note_id, member_id, patient_name, gender, age, location, note_date, note_type, provider_name, facility_name, icd_code, primary_diagnosis, subjective, objective, assessment, plan, follow_up_date
- `insurance_claims_mock.xlsx`: claim_id, member_id, patient_name, gender, age, location, date_of_service, claim_type, place_of_service, provider_name, facility_name, icd_code, diagnosis_description, cpt_code, procedure_description, billed_amount, claim_status
- `lab_results_mock.xlsx`: lab_id, member_id, patient_name, gender, age, draw_date, lab_type, test_name, result_value, unit, reference_range, result_flag, ordering_provider, lab_facility, status, clinical_note
- `medication_list_mock.xlsx`: med_id, member_id, patient_name, gender, age, drug_name, brand_name, dosage, route, frequency, indication, prescribing_provider, date_prescribed, last_fill_date, days_since_last_fill, adherence_status, medication_status, rx_notes
- `patient_demographics_mock.xlsx`: member_id, full_name, gender, age, date_of_birth, street_address, city, state, zip_code, location, phone_primary, phone_secondary, email_address, preferred_contact_method, preferred_language, marital_status, employment_status, caregiver_support, primary_conditions, insurance_plan_type, insurance_start_date, risk_tier, assigned_coordinator
- `pharmacy_claims_mock.xlsx`: rx_claim_id, member_id, patient_name, gender, age, date_filled, drug_name, brand_name, dosage, frequency, days_supply, quantity_dispensed, ndc_code, condition_treated, refill_number, refills_remaining, prescribing_provider, pharmacy_name, copay_amount, plan_paid_amount, fill_status
- `prior_auth_mock.xlsx`: auth_id, member_id, patient_name, gender, age, request_date, auth_type, service_requested, requesting_provider, decision, decision_date, valid_from, valid_through, denial_reason, appeal_status, auth_notes

## ngrok (Public URL for Local API)

Run app in one terminal:

```bash
python main.py
```

Expose port `8000` in another terminal:

```bash
ngrok http 8000
```

If first time using ngrok:

```bash
ngrok config add-authtoken YOUR_NGROK_TOKEN
```

Test health via public URL:

```text
https://<your-ngrok-domain>/api/v1/health
```

## CORS Behavior

- Origins: all allowed by default (`*`).
- Methods: all allowed.
- Headers: all allowed.
- Credentials: only enabled when explicitly set and non-wildcard origins are used.

## Tests

```bash
pytest -q
```
