from app.config import settings
from elasticsearch import Elasticsearch

es = Elasticsearch(
    settings.elasticsearch_url,
    headers={
        "Accept": "application/vnd.elasticsearch+json; compatible-with=8",
        "Content-Type": "application/vnd.elasticsearch+json; compatible-with=8"
    }
  )
PRODUCT_INDEX = "products"
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Or INFO, if you want less verbose logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def ensure_index():
    logger.info(f"Ensuring index '{PRODUCT_INDEX}' exists in Elasticsearch")
    if not es.indices.exists(index=PRODUCT_INDEX):
        logger.info(f"index '{PRODUCT_INDEX}' does not exist, creating it")
        es.indices.create(index=PRODUCT_INDEX, body={
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text"},
                    "slug": {"type": "keyword"},
                    "description": {"type": "text"},
                    "price_cents": {"type": "integer"},
                    "currency": {"type": "keyword"},
                    "inventory": {"type": "integer"},
                    "is_active": {"type": "boolean"},
                    "data": {"type": "object"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            }
        })
        logger.info(f"Index '{PRODUCT_INDEX}' created successfully")


def search_products(query: str, limit: int = 20):
    response = es.search(index=PRODUCT_INDEX, size=limit, body={
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "description", "data.color"]
            }
        }
    })
    return [hit["_source"] for hit in response["hits"]["hits"]]


def index_product(product):
    es.index(index=PRODUCT_INDEX, id=product.id, document={
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "description": product.description,
        "price_cents": product.price_cents,
        "currency": product.currency,
        "inventory": product.inventory,
        "is_active": product.is_active,
        "data": product.data,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat()
    })
