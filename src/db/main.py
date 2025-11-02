from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, select
from .config import Config
from src.model.Products import Product, ProductCategory
from src.model.User import User
from src.Auth.uitl import generate_hashed_password

async_engine = create_async_engine(url=Config.DATABASE_URL, echo=True)


async def init_db():

    async with async_engine.begin() as conn:
        # Lệnh này sẽ tạo các bảng (nếu chúng chưa tồn tại)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with Session() as session:
        yield session


async def create_default_admin():
    async with AsyncSession(async_engine) as session:
        statement = select(User).where(User.role == "admin")
        result = await session.exec(statement)
        admin_exists = result.first()

        if not admin_exists:
            admin_user = User(
                username="Admin",
                fullname="Administrator",
                email="admin123@gmail.com",
                hashed_password=generate_hashed_password("admin123"),
                role="admin",
                is_verified=True,
            )
            session.add(admin_user)
            await session.commit()
            print(
                "Default admin user created:",
            )
        else:
            print("Admin user already exists.")
