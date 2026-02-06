from fastapi import APIRouter, BackgroundTasks, Query
from typing import List
from schemas import ResponseModel, TicketItemSchema
from repository import db_ticket

router = APIRouter(prefix="/ticket", tags=["库存与SKU上报"])


@router.post("/report", response_model=ResponseModel)
async def report_inventory(items: List[TicketItemSchema], background_tasks: BackgroundTasks):
    """
    接收设备抓取到的 SKU 详细信息（支持批量上报）。

    业务逻辑：
    1. 接收来自 Frida 脚本或 Web 端抓取的项目、场次、票档数据。
    2. 使用 BackgroundTasks 异步执行数据库 UPSERT 操作，提高响应速度。
    """
    # 转换为字典列表以便 repository 处理
    rows = [item.dict() for item in items]

    # 异步入库：对应 ticket_mapper.yaml 中的 upsert_ticket_item
    background_tasks.add_task(db_ticket.upsert_ticket_items, rows)

    return ResponseModel(msg=f"已接收 {len(items)} 条库存记录，后台处理中")


@router.get("/available", response_model=ResponseModel)
async def get_available_inventory(item_id: str = Query(..., description="项目ID")):
    """
    查询指定项目当前所有“有票”的票档。

    业务场景：
    - 前端看板显示哪些票可以抢。
    - 调度逻辑判断是否需要唤醒抢票任务。
    """
    data = db_ticket.get_available_skus(item_id)
    return ResponseModel(data=data)


@router.get("/upcoming", response_model=ResponseModel)
async def get_upcoming_sales():
    """
    获取即将开售的项目列表（如 5 分钟内开抢）。
    """
    data = db_ticket.get_upcoming_sales()
    return ResponseModel(data=data)