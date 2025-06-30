from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/users")
def list_users():
    return [{"id": 1, "username": "models"}]
