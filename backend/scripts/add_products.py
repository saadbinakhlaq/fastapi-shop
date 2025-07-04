import asyncio
import json
from pathlib import Path

from app.crud.product import create_product
from app.database import sessionmanager  # adjust import if needed
from app.schemas.product import InProduct

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PRODUCTS_FILE = PROJECT_ROOT / "data" / "products.json"

async def seed_products():
    with open(PRODUCTS_FILE) as f:
        products_data = json.load(f)

    async with sessionmanager.session() as session:
        for product_dict in products_data:
            product = InProduct(**product_dict)
            await create_product(session, product)
        print(f"✅ Inserted {len(products_data)} products")

if __name__ == "__main__":
    asyncio.run(seed_products())
