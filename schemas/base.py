from pydantic import BaseModel
from typing import Any, Optional

class ResponseModel(BaseModel):
    code: int = 200
    msg: str = "success"
    data: Optional[Any] = None