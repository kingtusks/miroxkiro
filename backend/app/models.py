from pydantic import BaseModel
from typing import Optional


class LeaseAnalysisResponse(BaseModel):
    extracted_terms: Optional[dict] = None
    violations: Optional[list[dict]] = None
    missing_disclosures: Optional[list[dict]] = None
    summary: Optional[str] = None
    raw_analysis: Optional[str] = None


class DemandLetterRequest(BaseModel):
    tenant_name: str
    landlord_name: str
    address: str
    violations: list[dict]


class DemandLetterResponse(BaseModel):
    letter: str


class HPDViolationQuery(BaseModel):
    borough: str
    address: Optional[str] = None
    block: Optional[str] = None
    lot: Optional[str] = None
