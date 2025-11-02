from typing import List
from fastapi.security import HTTPBearer
from fastapi import Request, status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from .uitl import decode_access_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from src.model.User import User

user_service = UserService()


class TokenBearer(HTTPBearer):
    # this method create a autoerror
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_access_token(token)

        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token.",
            )
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or has been revoked",
                    "resolution": "Please get new token",
                },
            )

        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_access_token(token)

        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Subclasses must implement this method.")


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid access token.",
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid access token.",
            )


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_data = token_details["user"]

    if user_data["login_method"] == "email":
        user_identifier = user_data["email"]
    else:
        user_identifier = user_data["username"]

    user = await user_service.get_user_by_email_or_username(user_identifier, session)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


""""Get current user with uid"""
# async def get_current_user(
#     token_details: dict = Depends(AccessTokenBearer()),
#     session: AsyncSession = Depends(get_session),
# ):
#     user_data = token_details["user"]
#     uid = user_data["uid"]

#     user = await user_service.get_user_by_uid(uid, session)
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user


def require_roles(alowed_roles: List[str]):
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in alowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )
        return current_user

    return role_checker
