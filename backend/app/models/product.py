from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base, TimestampMixin


class Product(Base, TimestampMixin):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(index=True, unique=True)
    slug: Mapped[str] = mapped_column(index=True, unique=True)
    description: Mapped[str]
    price_cents: Mapped[int] = mapped_column(default=0)
    currency: Mapped[str] = mapped_column(default="USD")
    inventory: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

    data: Mapped[dict] = mapped_column(JSONB, default=dict)
