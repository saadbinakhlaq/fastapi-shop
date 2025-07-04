from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product as ProductDBModel
from app.schemas.product import InProduct


async def get_product(db_session: AsyncSession, product_id: int):
    product = (await db_session.scalars(select(ProductDBModel).where(ProductDBModel.id == product_id))).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

async def get_product_by_slug(db_session: AsyncSession, slug: str):
    return (await db_session.scalars(select(ProductDBModel).where(ProductDBModel.slug == slug))).first()

async def list_products(db_session: AsyncSession, skip: int = 0, limit: int = 20):
    stmt = select(ProductDBModel).offset(skip).limit(limit)
    return (await db_session.scalars(stmt)).all()

async def create_product(db_session: AsyncSession, product: InProduct):
    db_product = ProductDBModel(**product.model_dump())
    db_session.add(db_product)
    await db_session.commit()
    await db_session.refresh(db_product)
    return db_product
