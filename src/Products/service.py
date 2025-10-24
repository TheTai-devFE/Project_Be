from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .schema import CreateCategoryModel
from src.model.Products import ProductCategory


class CategoryService:
    async def create_category(
        self, cata_data: CreateCategoryModel, session: AsyncSession
    ):
        cata_data_dict = cata_data.model_dump()

        new_cata = ProductCategory(**cata_data_dict)

        session.add(new_cata)
        await session.commit()

        return new_cata

    async def get_all_cata(self, session: AsyncSession):
        statement = select(ProductCategory).order_by(desc(ProductCategory.created_at))

        result = await session.exec(statement)
        return result.all()

    async def get_cata_by_uid(self, cata_uid, session: AsyncSession):
        statement = select(ProductCategory).where(ProductCategory.uid == cata_uid)

        result = await session.exec(statement)
        cata = result.first()

        return cata if cata is not None else None

    async def update_cata(
        self, cata_uid: str, update_cata: CreateCategoryModel, session: AsyncSession
    ):
        cata_to_update = await self.get_cata_by_uid(cata_uid, session)

        if cata_to_update is not None:
            updata_data_dict = update_cata.model_dump()

            for k, v in updata_data_dict.items():
                setattr(cata_to_update, k, v)

                await session.commit()

                return cata_to_update
        else:
            return None

    async def delete_cata(self, cata_uid: str, session: AsyncSession):
        cata_to_delete = await self.get_cata_by_uid(cata_uid, session)

        if cata_to_delete is not None:
            await session.delete(cata_to_delete)

            await session.commit()

            return {}
        else:
            return None


class Product:
    async def get_all_product():
        pass
