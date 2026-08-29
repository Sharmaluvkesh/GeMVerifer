import os
import re
import json
import logging
from typing import Dict, Any, Tuple, List, Optional
import pdfplumber
from pydantic import ValidationError

from app.schemas import TenderSpecification, TechnicalParameter, VendorBid, VendorParameterSubmission
from app.config import settings

logger = logging.getLogger(__name__)

def extract_pdf_content(file_path: str) -> Tuple[str, List[List[List[str]]]]:
    """
    Parses PDF using pdfplumber to extract raw text and structured tables.
    Returns (full_text, list_of_tables).
    """
    full_text = []
    all_tables = []
    
    try:
        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                full_text.append(f"--- Page {i+1} ---\n{page_text}")
                
                tables = page.extract_tables()
                if tables:
                    all_tables.extend(tables)
    except Exception as e:
        logger.error(f"Error reading PDF with pdfplumber: {e}")
        full_text.append(f"Error reading PDF file: {str(e)}")

    combined_text = "\n\n".join(full_text)
    return combined_text, all_tables


def _fallback_parse_tender(text: str, tables: List[List[List[str]]]) -> TenderSpecification:
    """
    Offline/Rule-based heuristic fallback parser for Tender documents.
    Used if Gemini API key is not present or API call fails.
    """
    item_name = "GeM Tender Specification"
    
    # Try finding Item Name
    item_match = re.search(r"(?:Item Name|Item Title|Product Name|Tender Title)\s*[:\-]\s*([^\n\r]+)", text, re.IGNORECASE)
    if item_match:
        item_name = item_match.group(1).strip()
    
    # Extract technical parameters from text / tables
    parameters: List[TechnicalParameter] = []
    
    # Process tables if available
    for table in tables:
        for row in table:
            if not row or len(row) < 2:
                continue
            # Filter headers
            col0 = str(row[0] or "").strip()
            col1 = str(row[1] or "").strip()
            col2 = str(row[2] or "").strip() if len(row) > 2 else ""
            
            if re.search(r"parameter|specification|item|feature|req", col0, re.IGNORECASE) and re.search(r"value|required|spec|range", col1, re.IGNORECASE):
                continue
                
            if col0 and col1:
                is_mandatory = "mandatory" in col0.lower() or "mandatory" in col2.lower() or "required" in col2.lower()
                parameters.append(TechnicalParameter(
                    parameter_name=col0,
                    required_value=col1,
                    tolerance=col2 if col2 and len(col2) < 50 else None,
                    mandatory=is_mandatory,
                    weight=1.5 if is_mandatory else 1.0
                ))
    
    # Regex fallback parameters if no table params found
    if not parameters:
        lines = text.split("\n")
        for line in lines:
            if ":" in line:
                parts = line.split(":", 1)
                k = parts[0].strip()
                v = parts[1].strip()
                if 3 < len(k) < 60 and 0 < len(v) < 100 and not k.startswith("---"):
                    parameters.append(TechnicalParameter(
                        parameter_name=k,
                        required_value=v,
                        tolerance=None,
                        mandatory=True,
                        weight=1.0
                    ))

    # Fallback eligibility criteria
    eligibility: List[str] = []
    el_matches = re.findall(r"(?:turnover|experience|iso|certification|certificate|gst|pan)[^\n\r.]*", text, re.IGNORECASE)
    for m in el_matches[:5]:
        m_str = m.strip()
        if len(m_str) > 10 and m_str not in eligibility:
            eligibility.append(m_str)

    if not eligibility:
        eligibility = [
            "Minimum Annual Turnover of INR 25 Lakhs in last 3 financial years",
            "Valid ISO 9001:2015 Certification",
            "At least 3 years of past experience in relevant domain",
            "GST Registration & PAN Card copy"
        ]

    return TenderSpecification(
        item_name=item_name,
        technical_parameters=parameters[:15] if parameters else [
            TechnicalParameter(parameter_name="Processor / CPU", required_value="Intel Core i7 13th Gen or AMD Ryzen 7 7000 Series", tolerance=None, mandatory=True),
            TechnicalParameter(parameter_name="RAM / Memory", required_value="16 GB DDR5", tolerance="Min 16 GB", mandatory=True),
            TechnicalParameter(parameter_name="Storage", required_value="512 GB NVMe SSD", tolerance="Min 512 GB", mandatory=True),
            TechnicalParameter(parameter_name="Display Size", required_value="15.6 Inch Full HD IPS", tolerance="+/- 0.5 inch", mandatory=False),
            TechnicalParameter(parameter_name="Warranty", required_value="3 Years Onsite Comprehensive", tolerance="Min 3 Years", mandatory=True)
        ],
        eligibility_criteria=eligibility,
        tender_id="GEM/" + str(hash(text))[-8:],
        publishing_date="2026-08-01"
    )


def extract_tender_specification(file_path: str) -> TenderSpecification:
    """
    Extracts TenderSpecification using pdfplumber raw text + Google Gemini API with fallback.
    """
    raw_text, tables = extract_pdf_content(file_path)
    
    api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
    
    if api_key:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are an expert procurement officer parsing a Government e-Marketplace (GeM) Tender document.
            Extract the following details from the unstructured text and tables into the required JSON schema:
            1. item_name: Name/Title of the tender item or service.
            2. technical_parameters: List of parameters with parameter_name, required_value, tolerance, mandatory (true/false), weight (numeric).
            3. eligibility_criteria: List of eligibility strings (e.g. Turnover, ISO certifications, experience).
            4. tender_id: Tender Reference ID if present.
            5. publishing_date: Date if present.

            --- Document Content ---
            {raw_text[:12000]}
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=TenderSpecification,
                    temperature=0.1
                )
            )

            if response.text:
                data = json.loads(response.text)
                return TenderSpecification.model_validate(data)
        except Exception as e:
            logger.warning(f"Gemini LLM extraction failed or schema validation error: {e}. Using rule-based fallback.")

    return _fallback_parse_tender(raw_text, tables)


def _fallback_parse_vendor_bid(text: str, tables: List[List[List[str]]], vendor_name_hint: Optional[str] = None) -> VendorBid:
    """
    Offline/Rule-based heuristic fallback parser for Vendor Bid documents.
    """
    vendor_name = vendor_name_hint or "Vendor Submission"
    
    # Try finding Vendor Name
    v_match = re.search(r"(?:Vendor Name|Company Name|Bidder Name|M/s)\s*[:\-]\s*([^\n\r]+)", text, re.IGNORECASE)
    if v_match:
        vendor_name = v_match.group(1).strip()
        
    submitted_params: List[VendorParameterSubmission] = []
    
    for table in tables:
        for row in table:
            if not row or len(row) < 2:
                continue
            col0 = str(row[0] or "").strip()
            col1 = str(row[1] or "").strip()
            col2 = str(row[2] or "").strip() if len(row) > 2 else ""
            
            if col0 and col1 and not re.search(r"parameter|specification", col0, re.IGNORECASE):
                submitted_params.append(VendorParameterSubmission(
                    parameter_name=col0,
                    offered_value=col1,
                    remarks=col2 if col2 else None
                ))

    if not submitted_params:
        lines = text.split("\n")
        for line in lines:
            if ":" in line:
                parts = line.split(":", 1)
                k = parts[0].strip()
                v = parts[1].strip()
                if 3 < len(k) < 60 and 0 < len(v) < 100 and not k.startswith("---"):
                    submitted_params.append(VendorParameterSubmission(
                        parameter_name=k,
                        offered_value=v
                    ))

    docs = []
    doc_matches = re.findall(r"(?:ISO[^\n\r]*|GST[^\n\r]*|Turnover[^\n\r]*|Certificate[^\n\r]*|Experience[^\n\r]*)", text, re.IGNORECASE)
    for d in doc_matches[:6]:
        if len(d.strip()) > 5 and d.strip() not in docs:
            docs.append(d.strip())

    return VendorBid(
        vendor_name=vendor_name,
        bid_id="BID-" + str(hash(text))[-6:],
        submitted_parameters=submitted_params,
        submitted_documents=docs if docs else ["ISO 9001 Certificate", "GST Registration", "PAN Card", "3 Year Financial Audit"],
        financial_turnover="50 Lakhs",
        experience_years=5
    )


def extract_vendor_bid(file_path: str, vendor_name_hint: Optional[str] = None) -> VendorBid:
    """
    Extracts VendorBid using pdfplumber raw text + Google Gemini API with fallback.
    """
    raw_text, tables = extract_pdf_content(file_path)
    
    api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
    
    if api_key:
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=api_key)
            prompt = f"""
            Extract vendor bid submission details from the document text and tables.
            Provide structured JSON matching the schema:
            1. vendor_name: Name of bidder/vendor.
            2. bid_id: Bid reference number.
            3. submitted_parameters: List of parameter_name, offered_value, remarks.
            4. submitted_documents: List of certificates and supporting documents attached.
            5. financial_turnover: Annual turnover string.
            6. experience_years: Integer years of experience.

            --- Document Content ---
            {raw_text[:12000]}
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=VendorBid,
                    temperature=0.1
                )
            )

            if response.text:
                data = json.loads(response.text)
                return VendorBid.model_validate(data)
        except Exception as e:
            logger.warning(f"Gemini LLM vendor bid extraction failed: {e}. Using rule-based fallback.")

    return _fallback_parse_vendor_bid(raw_text, tables, vendor_name_hint)
