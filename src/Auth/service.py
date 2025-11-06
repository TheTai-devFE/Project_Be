from src.model.User import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schema import UserCreateModel, UserModel
from .uitl import generate_hashed_password


class UserService:
    async def get_all_users(self, session: AsyncSession):
        statement = select(User)
        result = await session.exec(statement)
        return result.all()

    async def get_user_by_uid(self, uid: str, session: AsyncSession):
        statement = select(User).where(User.uid == uid)
        result = await session.exec(statement)
        user = result.first()
        return user if user is not None else None

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

        new_user = User(**user_data_dict, role="user")
        new_user.hashed_password = generate_hashed_password(user_data_dict["password"])

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    # async def update_user(
    #     self,
    #     user: User,
    #     user_update: UserModel,
    #     session: AsyncSession,
    # ):

    #     user_data_dict = user_update.model_dump(exclude_unset=True)

    #     if "hashed_password" in user_data_dict:
    #         user_data_dict["hashed_password"] = generate_hashed_password(
    #             user_data_dict("hashed_password")
    #         )

    #     for k, v in user_data_dict.items():
    #         setattr(user, k, v)

    #     # user.role = new_role
    #     # session.add(user)
    #     await session.commit()
    #     await session.refresh(user)
    #     return user

    async def update_user(self, user, user_update, session):
        user_data_dict = user_update.model_dump(exclude_unset=True)

        user_data_dict = {
            k: v
            for k, v in user_data_dict.items()
            if v not in (None, "", "string")  # "string" là default Swagger
        }

        if "hashed_password" in user_data_dict:
            user_data_dict["hashed_password"] = generate_hashed_password(
                user_data_dict["hashed_password"]
            )

        for k, v in user_data_dict.items():
            setattr(user, k, v)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def delete_user(self, user_uid: str, session: AsyncSession):
        user_to_delete = await self.get_user_by_uid(user_uid, session)

        if user_to_delete is not None:
            await session.delete(user_to_delete)

            await session.commit()
            await session.refresh(user_to_delete)

            return {}
        else:
            return None
