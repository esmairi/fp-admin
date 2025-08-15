from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from fp_admin.api.error_handlers import handle_record_error, handle_validation_error
from fp_admin.core import get_session
from fp_admin.models.views.exceptions import FpValidationErrors

from ...providers.exceptions import AuthError
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
    signup_request: SignupRequest, session: AsyncSession = Depends(get_session)
) -> SignupResponse:
    user_service = UserService(session)
    try:
        return await user_service.create_user(signup_request.data)
    except FpValidationErrors as e:
        raise handle_validation_error(e.details) from e
    except Exception as e:
        raise handle_record_error(f"Unknow Error: {str(e)}") from e


# --- Signin Endpoint ---
@router.post("/signin", response_model=SigninResponse)
async def signin(
    request_data: SigninRequest,
    session: AsyncSession = Depends(get_session),
) -> SigninResponse:
    user_service = UserService(session)
    data = request_data.data
    try:
        token_data = await user_service.authenticate_and_issue_token(
            data.username, data.password
        )
    except AuthError as e:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED") from e
    if not token_data:
        raise HTTPException(status_code=401, detail="UNAUTHORIZED")

    return SigninResponse(data=token_data)


@router.post("/refresh")
async def refresh_token(
    payload: RefreshRequest,
    session: AsyncSession = Depends(get_session),
) -> Any:
    user_service = UserService(session)

    try:
        return await user_service.refresh_token(payload.refresh_token, payload.username)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from e
