from fastapi import APIRouter


router = APIRouter()


@router.get("/{id}")
async def get_user_by_id(id: int):
    pass