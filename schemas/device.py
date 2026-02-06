from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class DeviceSchema(BaseModel):
    sn: str = Field(..., description="设备SN码")
    brand: Optional[str] = None
    model: Optional[str] = None
    ip_address: Optional[str] = None
    status: int = 0


class DeviceGroupSchema(BaseModel):
    name: str
    config_json: Optional[Dict[str, Any]] = Field(None, description="组配置")
    description: Optional[str] = None


class GroupCreate(BaseModel):
    name: str
    config_json: Optional[Dict[str, Any]] = {"delay": 500, "thread_count": 5}
    description: Optional[str] = None


class GroupUpdate(BaseModel):
    config_json: Optional[Dict[str, Any]]
    description: Optional[str]


class MigrateRequest(BaseModel):
    """
    批量迁移设备分组的请求模型
    """
    sn_list: List[str] = Field(
        ...,
        min_length=1, # V2 中 min_items 也建议改为 min_length
        description="需要迁移的设备序列号(SN)列表",
    )
    target_group_id: int = Field(
        ...,
        description="目标分组的 ID (对应 device_groups 表的主键)",
    )

    # --- 核心修改点：消除警告 ---
    model_config = {
        "json_schema_extra": {
            "example": {
                "sn_list": ["PHONE_001", "PHONE_002"],
                "target_group_id": 10
            }
        }
    }
