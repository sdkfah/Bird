from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TicketItemSchema(BaseModel):
    item_id: str = Field(..., description="项目ID")
    project_title: Optional[str] = Field(None, description="演出名称")
    venue_name: Optional[str] = Field(None, description="场馆")
    perform_id: str = Field(..., description="场次ID")
    perform_time: Optional[datetime] = None
    sku_id: str = Field(..., description="票档SKU ID")
    price_name: Optional[str] = None
    price: Optional[float] = None
    stock_status: int = Field(1, description="是否有票: 1有, 0无")
    limit_quantity: int = 4
    sale_start_time: Optional[datetime] = None

    class Config:
        from_attributes = True