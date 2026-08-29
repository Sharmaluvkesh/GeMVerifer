export interface TechnicalParameter {
  parameter_name: str;
  required_value: string;
  tolerance?: string;
  mandatory: boolean;
  weight: number;
}

export interface TenderSpecification {
  item_name: string;
  technical_parameters: TechnicalParameter[];
  eligibility_criteria: string[];
  tender_id?: string;
  publishing_date?: string;
}

export interface ParameterComparisonResult {
  parameter_name: string;
  tender_required_value: string;
  tolerance?: string;
  vendor_offered_value: string;
  status: 'COMPLIANT' | 'NON_COMPLIANT' | 'NEEDS_REVIEW';
  is_mandatory: boolean;
  score: number;
  explanation: string;
}

export interface VendorEvaluationResult {
  vendor_name: string;
  bid_id?: string;
  technical_score: number;
  is_disqualified: boolean;
  disqualification_reasons: string[];
  missing_documents: string[];
  parameter_results: ParameterComparisonResult[];
}

export interface AnalysisReportResponse {
  report_id: string;
  tender_info: TenderSpecification;
  vendors: VendorEvaluationResult[];
  evaluated_at: string;
}
