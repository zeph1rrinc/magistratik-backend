from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Response
from fastapi import status

from ..models import players
from ..services.players import PlayersService

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", response_model=List[players.Player])
async def get_players(players_service: PlayersService = Depends()):
    return await players_service.get_many()


@router.post(
    "/",
    response_model=players.Player,
    status_code=status.HTTP_201_CREATED,
)
async def create_player(
    player_data: players.PlayerCreate,
    players_service: PlayersService = Depends(),
):
    return await players_service.create(player_data)


@router.get(
    "/{player_id}",
    response_model=players.Player,
)
async def get_player(player_id: UUID, players_service: PlayersService = Depends()):
    return await players_service.get(player_id)


@router.put(
    "/{player_id}",
    response_model=players.Player,
)
async def update_player(
    player_id: UUID,
    player_data: players.PlayerUpdate,
    players_service: PlayersService = Depends(),
):
    return await players_service.update(player_id, player_data)


@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_player(player_id: UUID, players_service: PlayersService = Depends()):
    await players_service.delete(player_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
