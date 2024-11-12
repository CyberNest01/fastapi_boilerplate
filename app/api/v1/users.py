from fastapi import APIRouter

from app.schemas.api_response import ApiResponse

router = APIRouter(
    prefix="/users",
    tags=["USER"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=ApiResponse)
async def get_users():
    return ApiResponse(status=True, message=None, data="test user")
