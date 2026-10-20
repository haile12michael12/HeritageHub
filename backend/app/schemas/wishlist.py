from datetime import datetime
from decimal import Decimal
from app.schemas.schema_base import SchemaBaseModel

class WishlistAdd(SchemaBaseModel):
    product_id: int

class WishlistItemRead(SchemaBaseModel):
    id: int
    product_id: int
    product_name: str | None = None
    product_price: Decimal | None = None
    product_image: str | None = None
    created_at: datetime
