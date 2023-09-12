from typing import Optional
from pydantic import BaseModel


class ProductViewModel(BaseModel):
    id: Optional[str]
    search: str
    price = int
    currency = str
    store = str
    description = str
    web = str
    uuid = str
