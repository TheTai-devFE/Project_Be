from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from .schema import UserCreateModel, UserModel, UserLoginModel
from .uitl import verify_password, create_access_token
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import timedelta

auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_account(
    user_data: UserCreateModel, session: AsyncSession = Depends(get_session)
):

    user_exists = await user_service.user_exists(
        user_data.email, user_data.username, session
    )
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    new_user = await user_service.create_user(user_data, session)
    return new_user


@auth_router.post("/login")
async def login_user(
    user_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    user = await user_service.get_user_by_email_or_username(
        user_data.identifier, session
    )

    if user is not None:
        password_valid = verify_password(user_data.password, user.hashed_password)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "uid": str(user.uid),
                    "username": user.username,
                    "email": user.email,
                }
            )
            resfresh_token = create_access_token(
                user_data={
                    "uid": str(user.uid),
                    "username": user.username,
                    "email": user.email,
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True,
            )
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": resfresh_token,
                    "user": {
                        "uid": str(user.uid),
                        "username": user.username,
                        "email": user.email,
                    },
                },
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid identifier Or Password"
    )


@auth_router.get("/", response_model=list[UserModel])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    users = await user_service.get_all_users(session)
    return users
