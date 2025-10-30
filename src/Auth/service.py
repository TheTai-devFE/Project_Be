from src.model.User import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schema import UserCreateModel
from .uitl import generate_hashed_password


class UserService:
    async def get_all_users(self, session: AsyncSession):
        statement = select(User)
        result = await session.exec(statement)
        return result.all()

    async def get_user_by_email_or_username(
        self, identifier: str, session: AsyncSession
    ):
        statement = select(User).where(
            (User.email == identifier) | (User.username == identifier)
        )
        result = await session.exec(statement)
        user = result.first()
        return user if user is not None else None

    async def user_exists(self, email: str, username: str, session: AsyncSession):
        statement = select(User).where(
            (User.email == email) | (User.username == username)
        )
        result = await session.exec(statement)
        user = result.first()
        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)
        new_user.hashed_password = generate_hashed_password(user_data_dict["password"])

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
