from pydantic import BaseModel, Field
from typing import Optional

class ActionLogSchema(BaseModel):
    device_sn: Optional[str] = None
    task_id: Optional[int] = None
    level: str = "INFO"
    module: Optional[str] = Field(None, description="Frida/ADB/Web")
    content: str

    class Config:
        from_attributes = True