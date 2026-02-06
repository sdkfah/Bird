from .base_repo import BaseRepository
from loguru import logger

class OrderRepository(BaseRepository):
    def __init__(self, mapper_dir):
        super().__init__(mapper_dir)

    def get_matchable_orders(self):
        """获取所有可以立即执行抢票的任务"""
        try:
            return self.execute("order_mapper", "find_matching_tasks", {})
        except Exception as e:
            logger.error(f"查询匹配任务失败: {e}")
            return []

    def mark_task_success(self, task_id):
        """标记任务为已抢到"""
        return self.execute("order_mapper", "update_task_status", {
            "task_id": task_id,
            "status": 1
        })