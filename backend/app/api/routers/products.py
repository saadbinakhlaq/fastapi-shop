import logging

from fastapi import APIRouter, Query

from app.schemas.product import OutProduct
from app.services.elasticsearch import search_products

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get(
    "/",
    response_model=list[OutProduct],
)
async def products(
    query: str = Query(..., min_length=2),
    limit: int = 10,
):
    """
    Get search products details
    """
    logger.debug(f"Searching products with query: {query} and limit: {limit}")
    products = search_products(query, limit)
    logger.info(f"Found {len(products)} products for query: {query}")
    if not products:
        logger.warning(f"No products found for query: {query}")
        return []
    return products
