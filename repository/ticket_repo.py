from .base_repo import BaseRepository
from loguru import logger
from typing import List, Dict

class TicketRepository(BaseRepository):
    def __init__(self, mapper_dir):
        super().__init__(mapper_dir)

    def upsert_ticket_items(self, items: List[Dict]):
        """
        批量更新或插入 SKU 库存信息
        items: 包含 item_id, sku_id, stock_status 等字段的列表
        """
        success_count = 0
        for item in items:
            try:
                # 执行 upsert_ticket_item 映射
                self.execute("ticket_mapper", "upsert_ticket_item", item)
                success_count += 1
            except Exception as e:
                logger.error(f"SKU {item.get('sku_id')} 更新失败: {e}")
        return success_count

    def get_available_skus(self, item_id: str):
        """
        查询特定项目当前所有“有票”的 SKU 列表
        """
        params = {"item_id": item_id}
        try:
            return self.execute("ticket_mapper", "get_available_skus", params)
        except Exception as e:
            logger.error(f"查询项目 {item_id} 可用库存失败: {e}")
            return []

    def get_stock_summary(self, item_id: str):
        """
        统计某个演出各价位的库存分布情况
        """
        params = {"item_id": item_id}
        try:
            return self.execute("ticket_mapper", "get_item_stock_summary", params)
        except Exception as e:
            logger.error(f"统计项目 {item_id} 库存分布失败: {e}")
            return []

    def get_upcoming_sales(self):
        """
        获取未来 5 分钟内即将开售的项目
        """
        try:
            return self.execute("ticket_mapper", "get_upcoming_sales")
        except Exception as e:
            logger.error(f"获取即将开售项目失败: {e}")
            return []