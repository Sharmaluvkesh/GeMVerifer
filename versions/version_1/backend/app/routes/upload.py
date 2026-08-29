import shutil
import uuid
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import TenderModel, BidModel
from app.schemas import TenderSpecification, VendorBid
from app.extractor import extract_tender_specification, extract_vendor_bid

router = APIRouter()

@router.post("/upload-tender")
async def upload_tender(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for GeM Tender upload.")
        
    file_id = str(uuid.uuid4())
    file_path = settings.UPLOAD_DIR / f"tender_{file_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        tender_spec: TenderSpecification = extract_tender_specification(str(file_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse tender PDF: {str(e)}")

    db_tender = TenderModel(
        id=file_id,
        tender_id=tender_spec.tender_id or f"GEM-{file_id[:6]}",
        item_name=tender_spec.item_name,
        file_path=str(file_path),
        extracted_data=tender_spec.model_dump()
    )
    db.add(db_tender)
    db.commit()
    db.refresh(db_tender)
    
    return {
        "status": "success",
        "tender_db_id": db_tender.id,
        "filename": file.filename,
        "specification": tender_spec
    }


@router.post("/upload-bid")
async def upload_bid(
    file: UploadFile = File(...),
    tender_db_id: Optional[str] = Form(None),
    vendor_name_hint: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for Vendor Bid upload.")

    # Validate tender existence if ID provided, or pick latest
    if tender_db_id:
        tender = db.query(TenderModel).filter(TenderModel.id == tender_db_id).first()
        if not tender:
            raise HTTPException(status_code=404, detail="Specified tender record not found.")
    else:
        tender = db.query(TenderModel).order_by(TenderModel.created_at.desc()).first()
        if not tender:
            raise HTTPException(status_code=400, detail="Please upload a Tender document before uploading Vendor Bids.")
        tender_db_id = tender.id

    file_id = str(uuid.uuid4())
    file_path = settings.UPLOAD_DIR / f"bid_{file_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        vendor_bid: VendorBid = extract_vendor_bid(
            str(file_path),
            vendor_name_hint=vendor_name_hint or Path(file.filename).stem
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse vendor bid PDF: {str(e)}")

    db_bid = BidModel(
        id=file_id,
        tender_id=tender_db_id,
        vendor_name=vendor_bid.vendor_name,
        bid_id=vendor_bid.bid_id or f"BID-{file_id[:6]}",
        file_path=str(file_path),
        extracted_data=vendor_bid.model_dump()
    )
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    
    return {
        "status": "success",
        "bid_db_id": db_bid.id,
        "tender_db_id": tender_db_id,
        "filename": file.filename,
        "vendor_bid": vendor_bid
    }
