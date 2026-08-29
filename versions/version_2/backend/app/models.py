import datetime
import uuid
from sqlalchemy import Column, String, Text, DateTime, JSON, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="BOTH")  # "VENDOR", "BIDDER", "BOTH"
    organization_name = Column(String, nullable=True)
    gstin = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    tenders = relationship("TenderModel", back_populates="user", cascade="all, delete-orphan")
    bids = relationship("BidModel", back_populates="user", cascade="all, delete-orphan")


class TenderModel(Base):
    __tablename__ = "tenders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    tender_id = Column(String, index=True, nullable=True)
    item_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    extracted_data = Column(JSON, nullable=False)  # Stores TenderSpecification JSON
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserModel", back_populates="tenders")
    bids = relationship("BidModel", back_populates="tender", cascade="all, delete-orphan")
    reports = relationship("ReportModel", back_populates="tender", cascade="all, delete-orphan")


class BidModel(Base):
    __tablename__ = "bids"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    tender_id = Column(String, ForeignKey("tenders.id"), nullable=False)
    vendor_name = Column(String, nullable=False)
    bid_id = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    extracted_data = Column(JSON, nullable=False)  # Stores VendorBid JSON
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("UserModel", back_populates="bids")
    tender = relationship("TenderModel", back_populates="bids")


class ReportModel(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tender_id = Column(String, ForeignKey("tenders.id"), nullable=False)
    evaluation_result = Column(JSON, nullable=False)  # Stores AnalysisReportResponse JSON
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    tender = relationship("TenderModel", back_populates="reports")
