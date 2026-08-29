from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ReportModel
from app.schemas import AnalysisReportResponse
from app.reporter import generate_pdf_report, generate_excel_report

router = APIRouter()

@router.get("/report/{report_id}", response_model=AnalysisReportResponse)
async def get_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    if report_id == "latest":
        report_record = db.query(ReportModel).order_by(ReportModel.created_at.desc()).first()
    else:
        report_record = db.query(ReportModel).filter(ReportModel.id == report_id).first()

    if not report_record:
        raise HTTPException(status_code=404, detail="Analysis report not found.")

    return AnalysisReportResponse.model_validate(report_record.evaluation_result)


@router.get("/report/export/{report_id}")
async def export_report(
    report_id: str,
    format: str = Query("pdf", description="Export format: 'pdf' or 'excel'"),
    db: Session = Depends(get_db)
):
    if report_id == "latest":
        report_record = db.query(ReportModel).order_by(ReportModel.created_at.desc()).first()
    else:
        report_record = db.query(ReportModel).filter(ReportModel.id == report_id).first()

    if not report_record:
        raise HTTPException(status_code=404, detail="Analysis report not found for export.")

    report_data = AnalysisReportResponse.model_validate(report_record.evaluation_result)

    if format.lower() == "excel":
        content = generate_excel_report(report_data)
        return Response(
            content=content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=GeM_Technical_Evaluation_{report_id[:8]}.xlsx"}
        )
    else:
        content = generate_pdf_report(report_data)
        return Response(
            content=content,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=GeM_Technical_Evaluation_{report_id[:8]}.pdf"}
        )
