from .base_repo import BaseRepository

class TicketRepository(BaseRepository):
    def batch_upsert_skus(self, rows):
        """批量同步库存数据"""
        for row in rows:
            # 调用 mappers/ticket_mapper.yaml 里的 upsert_sku
            self.execute("ticket_mapper", "upsert_sku", row)