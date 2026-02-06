from .base_repo import BaseRepository
from loguru import logger

class LogRepository(BaseRepository):
    def __init__(self, mapper_dir):
        super().__init__(mapper_dir)

    def _add_log(self, level, sn, content, module="System", task_id=None):
        """通用私有记录方法"""
        try:
            params = {
                "device_sn": sn,
                "task_id": task_id,
                "level": level,
                "module": module,
                "content": str(content)
            }
            self.execute("log_mapper", "insert_log", params)
        except Exception as e:
            # 如果写数据库日志失败，降级打印到控制台，防止程序崩溃
            logger.error(f"❌ 数据库日志写入失败: {e}")

    def info(self, sn, content, module="Frida", task_id=None):
        self._add_log("INFO", sn, content, module, task_id)

    def error(self, sn, content, module="Frida", task_id=None):
        self._add_log("ERROR", sn, content, module, task_id)

    def warning(self, sn, content, module="Frida", task_id=None):
        self._add_log("WARNING", sn, content, module, task_id)