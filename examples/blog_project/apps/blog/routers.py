from fastapi import APIRouter

router = APIRouter(prefix="/blog", tags=["blog"])


# @router.get("/custom_router")
# def get_data():
#     return my_data
