from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from fp_admin.core import get_session

from ...api.error_handlers import handle_model_error, handle_validation_error
from ...exceptions import ModelError, ValidationError
from .schemas import (
    RefreshRequest,
    SigninRequest,
    SigninResponse,
    SignupRequest,
    SignupResponse,
)
from .services import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


# --- Signup Endpoint ---
@router.post("/signup", response_model=SignupResponse, response_model_exclude_none=True)
async def signup(
    signup_request: SignupRequest, session: Session = Depends(get_session)
) -> SignupResponse:
    user_service = UserService(session)
    try:
        return user_service.create_user(signup_request.data)
    except ValidationError as e:
        raise handle_validation_error(e) from e
    except ModelError as e:
        raise handle_model_error(f"Failed to create user record: {str(e)}") from e
    except Exception as e:
        raise handle_model_error(f"Unknow Error: {str(e)}") from e


# --- Signin Endpoint ---
@router.post("/signin", response_model=SigninResponse)
async def signin(
    request_data: SigninRequest,
    session: Session = Depends(get_session),
) -> SigninResponse:
    user_service = UserService(session)
    data = request_data.data
    token_data = await user_service.authenticate_and_issue_token(
        data.username, data.password
    )
    if not token_data:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    return SigninResponse(data=token_data)


@router.post("/refresh")
async def refresh_token(
    payload: RefreshRequest,
    session: Session = Depends(get_session),
) -> Any:
    user_service = UserService(session)
    try:
        return user_service.refresh_token(payload.refresh_token, payload.username)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from e
