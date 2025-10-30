from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .service import ProductService
from .schema import ProductModel, ProductCreateModel, ProductUpdateModel
from src.db.main import get_session
from src.Auth.dependencies import AccessTokenBearer

product_router = APIRouter()
product_service = ProductService()
access_token_bearer = AccessTokenBearer()


@product_router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ProductCreateModel
)
async def create_product(
    product_data: ProductCreateModel, session: AsyncSession = Depends(get_session)
):
    product = await product_service.create_product(product_data, session)

    return product


@product_router.get("/", response_model=List[ProductModel])
async def get_all_products(
    session: AsyncSession = Depends(get_session),
    token_details=Depends(access_token_bearer),
):
    products = await product_service.get_all_products(session)
    return products


@product_router.get("/{product_uid}", response_model=ProductModel)
async def get_product(
    product_uid: str, session: AsyncSession = Depends(get_session)
) -> dict:
    product = await product_service.get_product(product_uid, session)

    if product:
        return product
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Product not found"},
        )


@product_router.patch("/{product_uid}", response_model=ProductModel)
async def update_product(
    product_uid: str,
    update_product: ProductCreateModel,
    session: AsyncSession = Depends(get_session),
):
    updated_product = await product_service.update_product(
        product_uid, update_product, session
    )

    if updated_product is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Update product False"
        )
    else:
        return updated_product


@product_router.delete("/{product_uid}", status_code=status.HTTP_202_ACCEPTED)
async def delete_product(
    product_uid: str, session: AsyncSession = Depends(get_session)
):
    product_to_delete = await product_service.delete_product(product_uid, session)

    if product_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Delete Product False"
        )
    else:
        return {"message": "Product deleted successfully"}
