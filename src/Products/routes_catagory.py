from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from .service import CategoryService
from .schema import CreateCategoryModel, CategoryModel
from src.db.main import get_session


cata_router = APIRouter()
cata_service = CategoryService()


@cata_router.post(
    "/", response_model=CategoryModel, status_code=status.HTTP_201_CREATED
)
async def create_category(
    cata_data: CreateCategoryModel, session: AsyncSession = Depends(get_session)
):
    new_cata = await cata_service.create_category(cata_data, session)

    return new_cata


@cata_router.get("/", response_model=List[CategoryModel])
async def get_all_catagory(session: AsyncSession = Depends(get_session)):
    catagories = await cata_service.get_all_cata(session)
    return catagories


@cata_router.get("/{cata_uid}", response_model=CategoryModel)
async def get_cata(cata_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    cata = await cata_service.get_cata_by_uid(cata_uid, session)

    if cata:
        return cata
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detai": "Catogory not found"},
        )


@cata_router.patch("/{cata_uid}", response_model=CategoryModel)
async def update_category(
    cata_uid: str,
    update_cata: CreateCategoryModel,
    session: AsyncSession = Depends(get_session),
):
    update_cata = await cata_service.update_cata(cata_uid, update_cata, session)

    if update_cata is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Update catagory False"
        )
    else:
        return update_cata


@cata_router.delete("/{cata_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cata(cata_uid: str, session: AsyncSession = Depends(get_session)):
    cata_to_delete = await cata_service.delete_cata(cata_uid, session)

    if cata_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Update catagory False"
        )
    else:
        return {"message": "Delete Catagory Is Successfully"}
