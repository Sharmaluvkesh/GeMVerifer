from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- User & Auth Schemas ---

class UserRegister(BaseModel):
    name: str = Field(..., description="Full Name of user/official")
    email: str = Field(..., description="Official Email Address")
    password: str = Field(..., min_length=6, description="Account Password")
    role: str = Field("BOTH", description="Role selection: 'VENDOR', 'BIDDER', or 'BOTH'")
    organization_name: Optional[str] = Field(None, description="Company / Department Name")
    gstin: Optional[str] = Field(None, description="GSTIN / Procurement Registration Code")

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str  # "VENDOR", "BIDDER", "BOTH"
    organization_name: Optional[str] = None
    gstin: Optional[str] = None
    created_at: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class DashboardStatsResponse(BaseModel):
    role: str
    active_persona: str  # "VENDOR" or "BUYER"
    total_tenders_published: int = 0
    total_bids_submitted: int = 0
    total_evaluations_run: int = 0
    average_compliance_score: float = 0.0
    disqualification_rate: float = 0.0
    recent_tenders: List[Dict[str, Any]] = Field(default_factory=list)
    recent_bids: List[Dict[str, Any]] = Field(default_factory=list)


# --- Technical Specification & Evaluation Schemas ---

class TechnicalParameter(BaseModel):
    parameter_name: str = Field(..., description="Name of the technical parameter/specification")
    required_value: str = Field(..., description="Required value or threshold specified in tender")
    tolerance: Optional[str] = Field(None, description="Permissible tolerance/range e.g. '+/- 5%' or 'Min 80%'")
    mandatory: bool = Field(True, description="Whether this parameter is mandatory for compliance")
    weight: float = Field(1.0, description="Weighting factor for scoring (default 1.0)")

class TenderSpecification(BaseModel):
    item_name: str = Field(..., description="Item or service name specified in the GeM tender")
    technical_parameters: List[TechnicalParameter] = Field(default_factory=list, description="List of technical parameters")
    eligibility_criteria: List[str] = Field(default_factory=list, description="List of eligibility requirements e.g. turnover, certifications, experience")
    tender_id: Optional[str] = Field(None, description="GeM Tender Reference Number/ID")
    publishing_date: Optional[str] = Field(None, description="Tender Issue Date")

class VendorParameterSubmission(BaseModel):
    parameter_name: str = Field(..., description="Parameter name as offered in bid")
    offered_value: str = Field(..., description="Value offered by the vendor")
    remarks: Optional[str] = Field(None, description="Additional specs or remarks")

class VendorBid(BaseModel):
    vendor_name: str = Field(..., description="Name of the bidding vendor")
    bid_id: Optional[str] = Field(None, description="Bid Reference Number")
    submitted_parameters: List[VendorParameterSubmission] = Field(default_factory=list)
    submitted_documents: List[str] = Field(default_factory=list, description="List of attached certificates/documents")
    financial_turnover: Optional[str] = Field(None, description="Vendor financial turnover")
    experience_years: Optional[int] = Field(None, description="Years of experience reported")

class ParameterComparisonResult(BaseModel):
    parameter_name: str
    tender_required_value: str
    tolerance: Optional[str] = None
    vendor_offered_value: str
    status: str  # "COMPLIANT", "NON_COMPLIANT", "NEEDS_REVIEW"
    is_mandatory: bool
    score: float  # 0.0 - 1.0
    explanation: str

class VendorEvaluationResult(BaseModel):
    vendor_name: str
    bid_id: Optional[str] = None
    technical_score: float  # 0 - 100%
    is_disqualified: bool
    disqualification_reasons: List[str] = Field(default_factory=list)
    missing_documents: List[str] = Field(default_factory=list)
    parameter_results: List[ParameterComparisonResult] = Field(default_factory=list)

class AnalysisReportResponse(BaseModel):
    report_id: str
    tender_info: TenderSpecification
    vendors: List[VendorEvaluationResult] = Field(default_factory=list)
    evaluated_at: str
