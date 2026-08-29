import re
import math
import logging
from difflib import SequenceMatcher
from typing import List, Tuple, Optional, Dict, Any

from app.schemas import (
    TenderSpecification,
    TechnicalParameter,
    VendorBid,
    VendorParameterSubmission,
    ParameterComparisonResult,
    VendorEvaluationResult
)

logger = logging.getLogger(__name__)

# Unit conversion constants for numeric specs
UNIT_MULTIPLIERS = {
    'tb': 1024.0,
    'gb': 1.0,
    'mb': 0.001,
    'ghz': 1000.0,
    'mhz': 1.0,
    'khz': 0.001,
    'lakh': 1.0,
    'lakhs': 1.0,
    'crore': 100.0,
    'crores': 100.0,
    'cr': 100.0,
    'l': 1.0,
    'year': 1.0,
    'years': 1.0,
    'yr': 1.0,
    'yrs': 1.0,
    'month': 1/12.0,
    'months': 1/12.0
}


def _extract_numeric_with_unit(text: str) -> Optional[Tuple[float, str]]:
    """
    Extracts numerical value and normalized unit from string.
    Example: '16 GB DDR5' -> (16.0, 'gb')
             '1.5 TB SSD' -> (1536.0, 'gb')
    """
    if not text:
        return None
        
    pattern = r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)?'
    matches = re.findall(pattern, text)
    if not matches:
        return None
        
    val_str, unit_str = matches[0]
    try:
        val = float(val_str)
        unit = unit_str.lower() if unit_str else ''
        
        # Apply unit multiplier if recognized
        multiplier = UNIT_MULTIPLIERS.get(unit, 1.0)
        base_unit = 'gb' if unit in ['tb', 'gb', 'mb'] else ('mhz' if unit in ['ghz', 'mhz', 'khz'] else unit)
        return (val * multiplier, base_unit)
    except ValueError:
        return None


def _calculate_string_similarity(str1: str, str2: str) -> float:
    """
    Calculates normalized string similarity score (0.0 to 1.0) using SequenceMatcher.
    """
    if not str1 or not str2:
        return 0.0
    s1 = re.sub(r'[^\w\s]', '', str1.lower()).strip()
    s2 = re.sub(r'[^\w\s]', '', str2.lower()).strip()
    
    if s1 == s2:
        return 1.0
    if s1 in s2 or s2 in s1:
        return 0.90
        
    return SequenceMatcher(None, s1, s2).ratio()


def match_single_parameter(
    tender_param: TechnicalParameter,
    vendor_submission: Optional[VendorParameterSubmission]
) -> ParameterComparisonResult:
    """
    Compares a single tender technical parameter against vendor submission.
    Implements Exact Matching, Numeric Range/Tolerance Check, and Semantic Text Matching.
    """
    req_val = tender_param.required_value
    tolerance = tender_param.tolerance or ""
    is_mandatory = tender_param.mandatory
    param_name = tender_param.parameter_name
    
    if not vendor_submission or not vendor_submission.offered_value:
        return ParameterComparisonResult(
            parameter_name=param_name,
            tender_required_value=req_val,
            tolerance=tolerance if tolerance else None,
            vendor_offered_value="NOT PROVIDED",
            status="NON_COMPLIANT" if is_mandatory else "NEEDS_REVIEW",
            is_mandatory=is_mandatory,
            score=0.0,
            explanation=f"Vendor did not provide any specification for mandatory parameter '{param_name}'." if is_mandatory else f"Parameter '{param_name}' not specified in vendor bid."
        )

    offered_val = vendor_submission.offered_value.strip()
    
    # 1. Check exact string equality
    if req_val.strip().lower() == offered_val.lower():
        return ParameterComparisonResult(
            parameter_name=param_name,
            tender_required_value=req_val,
            tolerance=tolerance if tolerance else None,
            vendor_offered_value=offered_val,
            status="COMPLIANT",
            is_mandatory=is_mandatory,
            score=1.0,
            explanation="Exact match with tender requirements."
        )
        
    # 2. Check Numeric Range & Tolerance
    req_num = _extract_numeric_with_unit(req_val)
    off_num = _extract_numeric_with_unit(offered_val)
    
    if req_num and off_num and req_num[1] == off_num[1]:
        req_val_num, unit = req_num
        off_val_num, _ = off_num
        
        # Check tolerance keywords (min, max, +/-)
        tol_lower = tolerance.lower() + " " + req_val.lower()
        
        if "min" in tol_lower or ">=" in tol_lower or "atleast" in tol_lower or "at least" in tol_lower:
            if off_val_num >= req_val_num:
                return ParameterComparisonResult(
                    parameter_name=param_name,
                    tender_required_value=req_val,
                    tolerance=tolerance if tolerance else None,
                    vendor_offered_value=offered_val,
                    status="COMPLIANT",
                    is_mandatory=is_mandatory,
                    score=1.0,
                    explanation=f"Offered numeric value ({offered_val}) satisfies minimum requirement ({req_val})."
                )
            else:
                deficit = req_val_num - off_val_num
                return ParameterComparisonResult(
                    parameter_name=param_name,
                    tender_required_value=req_val,
                    tolerance=tolerance if tolerance else None,
                    vendor_offered_value=offered_val,
                    status="NON_COMPLIANT",
                    is_mandatory=is_mandatory,
                    score=0.0,
                    explanation=f"Offered numeric value ({offered_val}) is below minimum requirement ({req_val}) by {deficit:.1f} {unit}."
                )

        elif "max" in tol_lower or "<=" in tol_lower:
            if off_val_num <= req_val_num:
                return ParameterComparisonResult(
                    parameter_name=param_name,
                    tender_required_value=req_val,
                    tolerance=tolerance if tolerance else None,
                    vendor_offered_value=offered_val,
                    status="COMPLIANT",
                    is_mandatory=is_mandatory,
                    score=1.0,
                    explanation=f"Offered value ({offered_val}) satisfies maximum requirement ({req_val})."
                )
            else:
                return ParameterComparisonResult(
                    parameter_name=param_name,
                    tender_required_value=req_val,
                    tolerance=tolerance if tolerance else None,
                    vendor_offered_value=offered_val,
                    status="NON_COMPLIANT",
                    is_mandatory=is_mandatory,
                    score=0.0,
                    explanation=f"Offered value ({offered_val}) exceeds maximum threshold ({req_val})."
                )
        else:
            # Default numeric comparison (Equal or greater for standard specs)
            if off_val_num >= req_val_num:
                return ParameterComparisonResult(
                    parameter_name=param_name,
                    tender_required_value=req_val,
                    tolerance=tolerance if tolerance else None,
                    vendor_offered_value=offered_val,
                    status="COMPLIANT",
                    is_mandatory=is_mandatory,
                    score=1.0,
                    explanation=f"Offered specification ({offered_val}) meets or exceeds required value ({req_val})."
                )
            else:
                return ParameterComparisonResult(
                    parameter_name=param_name,
                    tender_required_value=req_val,
                    tolerance=tolerance if tolerance else None,
                    vendor_offered_value=offered_val,
                    status="NON_COMPLIANT",
                    is_mandatory=is_mandatory,
                    score=0.0,
                    explanation=f"Offered value ({offered_val}) is inferior to required specification ({req_val})."
                )

    # 3. Semantic / Fuzzy Matching for Descriptive Specs
    similarity = _calculate_string_similarity(req_val, offered_val)
    
    if similarity >= 0.80:
        return ParameterComparisonResult(
            parameter_name=param_name,
            tender_required_value=req_val,
            tolerance=tolerance if tolerance else None,
            vendor_offered_value=offered_val,
            status="COMPLIANT",
            is_mandatory=is_mandatory,
            score=1.0,
            explanation=f"High semantic equivalence ({similarity*100:.0f}%) with tender requirement."
        )
    elif similarity >= 0.55:
        return ParameterComparisonResult(
            parameter_name=param_name,
            tender_required_value=req_val,
            tolerance=tolerance if tolerance else None,
            vendor_offered_value=offered_val,
            status="NEEDS_REVIEW",
            is_mandatory=is_mandatory,
            score=0.5,
            explanation=f"Partial descriptive match ({similarity*100:.0f}% similarity). Manual technical committee verification required."
        )
    else:
        return ParameterComparisonResult(
            parameter_name=param_name,
            tender_required_value=req_val,
            tolerance=tolerance if tolerance else None,
            vendor_offered_value=offered_val,
            status="NON_COMPLIANT",
            is_mandatory=is_mandatory,
            score=0.0,
            explanation=f"Offered specification ('{offered_val}') does not match tender requirement ('{req_val}')."
        )


def evaluate_vendor_against_tender(
    tender_spec: TenderSpecification,
    vendor_bid: VendorBid
) -> VendorEvaluationResult:
    """
    Evaluates a Vendor Bid against a Tender Specification.
    Returns complete VendorEvaluationResult with score, compliance status, and discrepancies.
    """
    parameter_results: List[ParameterComparisonResult] = []
    disqualification_reasons: List[str] = []
    
    # Map vendor submitted parameters by normalized name
    vendor_param_map: Dict[str, VendorParameterSubmission] = {}
    for sub in vendor_bid.submitted_parameters:
        norm_key = re.sub(r'[^\w]', '', sub.parameter_name.lower())
        vendor_param_map[norm_key] = sub
        
    total_weighted_score = 0.0
    total_max_weight = 0.0
    is_disqualified = False
    
    for tender_param in tender_spec.technical_parameters:
        weight = tender_param.weight if tender_param.weight > 0 else 1.0
        total_max_weight += weight
        
        # Try finding parameter match by name
        norm_name = re.sub(r'[^\w]', '', tender_param.parameter_name.lower())
        
        matched_vendor_sub = vendor_param_map.get(norm_name)
        if not matched_vendor_sub:
            # Try fuzzy match on parameter name
            best_match = None
            best_score = 0.0
            for v_key, v_sub in vendor_param_map.items():
                sim = _calculate_string_similarity(tender_param.parameter_name, v_sub.parameter_name)
                if sim > best_score:
                    best_score = sim
                    best_match = v_sub
            if best_score >= 0.65:
                matched_vendor_sub = best_match

        res = match_single_parameter(tender_param, matched_vendor_sub)
        parameter_results.append(res)
        
        total_weighted_score += res.score * weight
        
        if res.is_mandatory and res.status == "NON_COMPLIANT":
            is_disqualified = True
            disqualification_reasons.append(
                f"Failed mandatory technical parameter '{res.parameter_name}': {res.explanation}"
            )

    # Calculate overall technical score percentage (0 - 100%)
    technical_score = round((total_weighted_score / total_max_weight) * 100.0, 2) if total_max_weight > 0 else 0.0
    
    # Check Eligibility Criteria & Missing Documents
    missing_docs: List[str] = []
    vendor_docs_str = " ".join(vendor_bid.submitted_documents).lower()
    
    for criterion in tender_spec.eligibility_criteria:
        c_lower = criterion.lower()
        if "iso" in c_lower and "iso" not in vendor_docs_str:
            missing_docs.append("ISO Quality Certificate")
        elif "turnover" in c_lower and "turnover" not in vendor_docs_str and "audit" not in vendor_docs_str:
            missing_docs.append("Financial Turnover Certificate / Audited Statements")
        elif "experience" in c_lower and "experience" not in vendor_docs_str and "past" not in vendor_docs_str:
            missing_docs.append("Past Experience / Purchase Order Copies")
        elif "gst" in c_lower and "gst" not in vendor_docs_str:
            missing_docs.append("GST Registration Certificate")

    if missing_docs and not is_disqualified:
        disqualification_reasons.append(f"Missing mandatory eligibility documents: {', '.join(missing_docs)}")

    return VendorEvaluationResult(
        vendor_name=vendor_bid.vendor_name,
        bid_id=vendor_bid.bid_id,
        technical_score=technical_score,
        is_disqualified=is_disqualified,
        disqualification_reasons=disqualification_reasons,
        missing_documents=missing_docs,
        parameter_results=parameter_results
    )
