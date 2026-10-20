from typing import Generic, TypeVar, List
from pydantic import BaseModel
from math import ceil

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

    @classmethod
    def create(cls, items: List[T], total: int, page: int, page_size: int):
        total_pages = ceil(total / page_size) if page_size else 1
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )

def paginate_params(page: int = 1, page_size: int = 12, max_page_size: int = 50):
    page = max(1, page)
    page_size = min(max(1, page_size), max_page_size)
    offset = (page - 1) * page_size
    return page, page_size, offset
