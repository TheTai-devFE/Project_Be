from typing import Optional, List
from fastapi import HTTPException, status
from datetime import datetime
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select, desc
from .schema import CreateCategoryModel, ProductCreateModel, ProductUpdateModel
from src.model.Products import ProductCategory, Product


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

    async def get_cata_by_uid(self, cata_uid: str, session: AsyncSession):
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
            await session.refresh(cata_to_delete)

            return {}
        else:
            return None


class ProductService:
    async def get_all_products(self, session: AsyncSession):
        statement = (
            select(Product)
            .options(selectinload(Product.category))
            .order_by(desc(Product.created_at))
        )

        result = await session.exec(statement)

        return result.all()

    async def get_product(self, product_uid: str, session: AsyncSession):
        statement = select(Product).where(Product.uid == product_uid)
        result = await session.exec(statement)
        product = result.first()

        return product if product is not None else None

    async def create_product(
        self, product_data: ProductCreateModel, session: AsyncSession
    ):
        try:
            product_data_dict = product_data.model_dump()

            new_product = Product(**product_data_dict)

            session.add(new_product)
            await session.commit()

            return new_product
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create product: {str(e)}",
            )

    async def update_product(
        self,
        product_uid: str,
        update_product: ProductUpdateModel,
        session: AsyncSession,
    ):
        try:
            product_to_update = await self.get_product(product_uid, session)

            if not product_to_update:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found",
                )
            update_data_dict = update_product.model_dump(exclude_unset=True)

            for field, value in update_data_dict.items():
                setattr(product_to_update, field, value)

            product_to_update.updated_at = datetime.now()

            await session.commit()
            await session.refresh(product_to_update)
            return product_to_update
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to update product: {str(e)}",
            )

    async def delete_product(self, product_uid: str, session: AsyncSession):
        product_to_delete = await self.get_product(product_uid, session)

        if product_to_delete is not None:
            await session.delete(product_to_delete)

            await session.commit()

            return {"message": "Product deleted successfully"}
        else:
            return None
