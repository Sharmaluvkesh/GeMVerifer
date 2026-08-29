from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserModel
from app.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register", response_model=TokenResponse)
async def register_user(
    payload: UserRegister,
    db: Session = Depends(get_db)
):
    # Normalize email
    email_clean = payload.email.lower().strip()
    
    # Check if user already exists
    existing_user = db.query(UserModel).filter(UserModel.email == email_clean).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists. Please login instead."
        )

    # Validate role input
    role_upper = payload.role.upper().strip()
    if role_upper not in ["VENDOR", "BIDDER", "BOTH"]:
        role_upper = "BOTH"

    db_user = UserModel(
        name=payload.name.strip(),
        email=email_clean,
        hashed_password=hash_password(payload.password),
        role=role_upper,
        organization_name=payload.organization_name,
        gstin=payload.gstin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_access_token(user_id=db_user.id, email=db_user.email, role=db_user.role)

    user_resp = UserResponse(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email,
        role=db_user.role,
        organization_name=db_user.organization_name,
        gstin=db_user.gstin,
        created_at=db_user.created_at.isoformat() if db_user.created_at else None
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=user_resp
    )


@router.post("/login", response_model=TokenResponse)
async def login_user(
    payload: UserLogin,
    db: Session = Depends(get_db)
):
    email_clean = payload.email.lower().strip()
    user = db.query(UserModel).filter(UserModel.email == email_clean).first()
    
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password credentials."
        )

    token = create_access_token(user_id=user.id, email=user.email, role=user.role)

    user_resp = UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role,
        organization_name=user.organization_name,
        gstin=user.gstin,
        created_at=user.created_at.isoformat() if user.created_at else None
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=user_resp
    )


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: UserModel = Depends(get_current_user)
):
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role,
        organization_name=current_user.organization_name,
        gstin=current_user.gstin,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None
    )
