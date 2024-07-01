from fastapi import APIRouter

from .api_v1.users import users

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])