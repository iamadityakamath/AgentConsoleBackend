"""Base Pydantic schemas."""
from datetime import datetime
from typing import Generic, TypeVar, Optional, Any


T = TypeVar("T")


class BaseSchema:
    """Base schema for all Pydantic models."""
    pass


class ResponseSchema(Generic[T]):
    """
    Generic response schema.
    
    Attributes:
        success: Whether the request was successful
        message: Response message
        data: Response data
        timestamp: Response timestamp
    """
    success: bool
    message: str
    data: Optional[T] = None
    timestamp: datetime = None
    
    def __init__(self, success: bool, message: str, data: Optional[T] = None):
        self.success = success
        self.message = message
        self.data = data
        self.timestamp = datetime.utcnow()


class PaginationSchema:
    """
    Pagination schema.
    
    Attributes:
        page: Current page number
        page_size: Number of items per page
        total: Total number of items
        pages: Total number of pages
    """
    page: int
    page_size: int
    total: int
    pages: int
