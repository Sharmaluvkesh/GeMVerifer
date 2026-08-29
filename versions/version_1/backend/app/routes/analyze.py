import uuid
import datetime
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TenderModel, BidModel, ReportModel
from app.schemas import TenderSpecification, VendorBid, VendorEvaluationResult, AnalysisReportResponse
from app.comparator import evaluate_vendor_against_tender

router = APIRouter()

class AnalyzeRequest(BaseModel):
    tender_db_id: Optional[str] = None
    bid_db_ids: Optional[List[str]] = None

@router.post("/analyze", response_model=AnalysisReportResponse)
async def analyze_bids(
    payload: Optional[AnalyzeRequest] = None,
    db: Session = Depends(get_db)
):
    tender_db_id = payload.tender_db_id if payload else None
    bid_db_ids = payload.bid_db_ids if payload else None

    # Fetch target Tender
    if tender_db_id:
        tender_record = db.query(TenderModel).filter(TenderModel.id == tender_db_id).first()
    else:
        tender_record = db.query(TenderModel).order_by(TenderModel.created_at.desc()).first()

    if not tender_record:
        raise HTTPException(status_code=404, detail="No tender record found to analyze. Please upload a tender PDF first.")

    tender_spec = TenderSpecification.model_validate(tender_record.extracted_data)

    # Fetch Bids to evaluate
    query = db.query(BidModel).filter(BidModel.tender_id == tender_record.id)
    if bid_db_ids:
        query = query.filter(BidModel.id.in_(bid_db_ids))
    
    bid_records = query.all()
    if not bid_records:
        raise HTTPException(status_code=400, detail="No vendor bids found for this tender. Please upload vendor bid PDFs.")

    evaluated_vendors: List[VendorEvaluationResult] = []
    for bid_rec in bid_records:
        v_bid = VendorBid.model_validate(bid_rec.extracted_data)
        eval_res = evaluate_vendor_against_tender(tender_spec, v_bid)
        evaluated_vendors.append(eval_res)

    report_id = str(uuid.uuid4())
    report_response = AnalysisReportResponse(
        report_id=report_id,
        tender_info=tender_spec,
        vendors=evaluated_vendors,
        evaluated_at=datetime.datetime.utcnow().isoformat()
    )

    db_report = ReportModel(
        id=report_id,
        tender_id=tender_record.id,
        evaluation_result=report_response.model_dump()
    )
    db.add(db_report)
    db.commit()

    return report_response
