from typing import Any, List
from uuid import UUID

import aiohttp
import bcrypt
from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import APIRouter, Depends, HTTPException
import requests
from async_fastapi_jwt_auth.exceptions import MissingTokenError, JWTDecodeError
from starlette.responses import Response
from typing import List
from fastapi import Body
from app.core.config import settings
from app.deps.db import CurrentAsyncSession

from app.deps.request_params import ItemRequestParams
from app.deps.users import hash_password, encode_password
from app.models.client import Client
from app.models.user import User
from app.repo.user_repo import UserRepo
from app.schemas.client import ClientRead, ClientCreate
from app.schemas.tokens import Tokens
from app.schemas.user import UserRead, UserCreate, UserLogin, UserUpdate

router = APIRouter(prefix="/users")
auth_dep = AuthJWTBearer()


@AuthJWT.load_config
def get_config():
    return settings


@router.post("/register", response_model=UserRead)
async def register_user(
    user: UserCreate,
    session: CurrentAsyncSession,
):
    user_repo: UserRepo = UserRepo(session)
    hashed_password = hash_password(user.password)
    check_user = await user_repo.get_user_by_login(user.login)
    if check_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = UserCreate(
        surname=user.surname,
        name=user.name,
        middle_name=user.middle_name,
        login=user.login,
        password=hashed_password,
    )
    user = User(**user.model_dump())
    result = await user_repo.create_user(user)
    return result


@router.post("/login", response_model=Tokens)
async def login_user(
    user: UserLogin,
    session: CurrentAsyncSession,
):
    user_repo: UserRepo = UserRepo(session)
    db_user = await user_repo.get_user_by_login(user.login)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not bcrypt.checkpw(user.password.encode(), db_user.password.encode()):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    async with aiohttp.ClientSession() as session:
        result = await session.post(
            url="http://auth-service:8001/api/v1/auth/access_token",
            params={"user_id": db_user.id},
        )
        tokens = await result.json()

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }


@router.post("/refresh")
async def refresh_token(
    refresh_token: str,
    session: CurrentAsyncSession,
):
    async with aiohttp.ClientSession() as session:
        result = await session.post(
            url="http://auth-service:8001/api/v1/auth/refresh_token",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )
        tokens = await result.json()

    return {"access_token": tokens["access_token"]}


@router.get("/clients", response_model=List[ClientRead])
async def user_clients(
    session: CurrentAsyncSession, authorize: AuthJWT = Depends(auth_dep)
):
    await authorize.jwt_required()
    user_id = await authorize.get_jwt_subject()
    user_repo: UserRepo = UserRepo(session)
    clients: List = await user_repo.get_users_clients(user_id)
    return clients


@router.post("/create_client", response_model=ClientCreate)
async def create_client(
    client: ClientCreate,
    session: CurrentAsyncSession,
    authorize: AuthJWT = Depends(auth_dep),
):
    await authorize.jwt_required()
    user_repo: UserRepo = UserRepo(session)
    responsible_user = await user_repo.get_user_by_id(client.responsible_user_id)
    if not responsible_user:
        raise HTTPException(status_code=400, detail="User not found")
    client = Client(**client.model_dump())
    result = await user_repo.create_client(client)
    return result


@router.put("/update_client", response_model=ClientRead)
async def update_client(
    client_id: int,
    status: str,
    session: CurrentAsyncSession,
    authorize: AuthJWT = Depends(auth_dep),
):
    await authorize.jwt_required()
    user_repo: UserRepo = UserRepo(session)
    client = await user_repo.update_client_status(client_id, status)
    return client


@router.delete("/delete_clients")
async def delete_clients(
    session: CurrentAsyncSession,
    client_ids: List[int],
    authorize: AuthJWT = Depends(auth_dep),
):
    await authorize.jwt_required()
    user_repo: UserRepo = UserRepo(session)
    await user_repo.delete_clients(client_ids)
    return {"detail": "Clients have been deleted"}
