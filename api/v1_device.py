from fastapi import APIRouter, HTTPException
from schemas import ResponseModel, DeviceSchema, GroupCreate, MigrateRequest
from repository import db_device

router = APIRouter(prefix="/devices", tags=["设备与分组管理"])

@router.post("/register", response_model=ResponseModel)
async def register(device: DeviceSchema):
    """设备注册与状态更新"""
    db_device.register_device(device.dict())
    return ResponseModel(msg="设备注册成功")

@router.post("/{sn}/heartbeat", response_model=ResponseModel)
async def heartbeat(sn: str):
    """更新设备心跳"""
    db_device.update_heartbeat(sn)
    return ResponseModel(msg="心跳已接收")

@router.post("/migrate", response_model=ResponseModel)
async def migrate(req: MigrateRequest):
    """一键迁移设备分组"""
    count = db_device.migrate_devices_to_group(req.sn_list, req.target_group_id)
    return ResponseModel(msg=f"成功迁移 {count} 台设备")

# --- 分组相关接口 (Group CRUD) ---

@router.post("/groups", response_model=ResponseModel)
async def create_group(group: GroupCreate):
    """创建新设备分组及配置"""
    db_device.create_group(group.name, group.config_json, group.description)
    return ResponseModel(msg="分组创建成功")

@router.get("/groups", response_model=ResponseModel)
async def list_groups():
    """获取全部分组列表"""
    groups = db_device.get_all_groups()
    return ResponseModel(data=groups)

@router.get("/groups/{group_id}/members", response_model=ResponseModel)
async def get_group_members(group_id: int):
    """查看特定分组下的所有设备"""
    members = db_device.get_group_members(group_id)
    return ResponseModel(data=members)

@router.put("/groups/{group_id}", response_model=ResponseModel)
async def update_group(group_id: int, group: GroupCreate):
    """修改分组配置 (JSON) 或描述"""
    # 逻辑：更新 device_groups 表的 config_json 字段
    params = group.dict()
    params["id"] = group_id
    db_device.execute("device_mapper", "update_group", params)
    return ResponseModel(msg="分组更新成功")

@router.delete("/groups/{group_id}", response_model=ResponseModel)
async def delete_group(group_id: int):
    """删除设备分组"""
    # 注意：建议在业务层先检查该组下是否还有设备
    db_device.delete_group(group_id)
    return ResponseModel(msg="分组已删除")