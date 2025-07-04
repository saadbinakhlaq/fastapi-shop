from app.database import sessionmanager
from app.models import Product
from app.services.elasticsearch import index_product
from sqlalchemy import select


async def sync_all_products():
    async with sessionmanager.session() as session:
        products = await session.execute(select(Product))
        for p in products.scalars():
            index_product(p)

if __name__ == "__main__":
    import asyncio
    asyncio.run(sync_all_products())
    print("✅ Synced all products to Elasticsearch")
