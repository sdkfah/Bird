from .base_repo import BaseRepository
from loguru import logger

class TaskRepository(BaseRepository):
    def __init__(self, mapper_dir):
        super().__init__(mapper_dir)

    def get_pending_tasks(self):
        """
        获取所有待处理（status=0）的任务列表
        """
        try:
            return self.execute("task_mapper", "get_pending_tasks")
        except Exception as e:
            logger.error(f"获取待处理任务失败: {e}")
            return []

    def update_task_status(self, task_id: int, status: int):
        """
        更新任务状态 (例如: 1-成功, 2-失败)
        """
        params = {
            "id": task_id,
            "status": status
        }
        try:
            return self.execute("task_mapper", "update_task_status", params)
        except Exception as e:
            logger.error(f"更新任务 {task_id} 状态失败: {e}")
            raise

    def find_tasks_by_artist(self, artist_name: str):
        """
        根据艺人姓名模糊匹配待处理任务
        """
        params = {"artist": artist_name}
        try:
            return self.execute("task_mapper", "find_tasks_by_artist", params)
        except Exception as e:
            logger.error(f"搜索艺人 {artist_name} 相关任务失败: {e}")
            return []


    def get_matchable_task(self):
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