from fastapi import APIRouter, BackgroundTasks
from schemas import ActionLogSchema, ResponseModel
from repository import db_log

router = APIRouter(prefix="/logs", tags=["监控与日志"])

@router.post("/report", response_model=ResponseModel)
async def report_log(log: ActionLogSchema, background_tasks: BackgroundTasks):
    """异步上报设备运行日志"""
    background_tasks.add_task(
        db_log.info,
        sn=log.device_sn,
        content=log.content,
        module=log.module,
        task_id=log.task_id
    )
    return ResponseModel(msg="日志已入库队列")