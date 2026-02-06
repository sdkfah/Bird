from fastapi import APIRouter
from schemas import ResponseModel, OrderTaskSchema
from repository import db_task


router = APIRouter(prefix="/tasks", tags=["抢票任务管理"])

@router.get("/poll/{sn}", response_model=ResponseModel)
async def poll_tasks(sn: str):
    """设备拉取待认领的抢票任务"""
    tasks = db_task.get_matchable_task()
    return ResponseModel(data=tasks)

@router.put("/{task_id}/status", response_model=ResponseModel)
async def update_status(task_id: int, status: int):
    """反馈任务执行结果（成功/失败）"""
    db_task.update_task_status(task_id, status)
    return ResponseModel(msg="状态已更新")