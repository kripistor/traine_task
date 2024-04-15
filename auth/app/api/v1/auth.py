import bcrypt
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import FastAPI, HTTPException, Depends, Request, APIRouter
from async_fastapi_jwt_auth import AuthJWT

from app.core.config import settings

router = APIRouter(prefix="/auth")

auth_dep = AuthJWTBearer()


@AuthJWT.load_config
def get_config():
    return settings


@router.post("/access_token")
async def login(user_id: int, authorize: AuthJWT = Depends(auth_dep)):
    access_token = await authorize.create_access_token(
        subject=user_id
    )
    refresh_token = await authorize.create_refresh_token(
        subject=user_id
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh_token")
async def refresh(authorize: AuthJWT = Depends(auth_dep)):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    await authorize.jwt_refresh_token_required()

    current_user = await authorize.get_jwt_subject()
    new_access_token = await authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}