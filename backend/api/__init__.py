from fastapi import APIRouter

from . import players

router = APIRouter()
router.include_router(players.router)
