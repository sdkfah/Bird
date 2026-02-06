# repository/__init__.py
from .order_repo import OrderRepository
from .ticket_repo import TicketRepository

import os

# 获取 mapper 文件夹的绝对路径
MAPPER_PATH = os.path.join(os.path.dirname(__file__), '..', 'mappers')

# 实例化 db_order，它会自动加载 mappers 里的 SQL 模板
db_order = OrderRepository(MAPPER_PATH)
db_ticket = TicketRepository(MAPPER_PATH)