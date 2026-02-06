from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class OrderTaskSchema(BaseModel):
    id: Optional[int] = None
    city: str
    artist: str
    target_date: Optional[date] = None
    target_price: Optional[float] = None
    customer_info: Optional[str] = Field(None, description="实名人信息(姓名+身份证)")
    priority_order: Optional[str] = None
    bounty: Optional[float] = None
    contact_phone: Optional[str] = None
    status: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True