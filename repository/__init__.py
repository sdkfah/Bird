# repository/__init__.py
import os
from .base_repo import BaseRepository
from .device_repo import DeviceRepository
from .log_repo import LogRepository
from .ticket_repo import TicketRepository
from .task_repo import TaskRepository

MAPPER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mappers')


db_device = DeviceRepository(MAPPER_PATH)
db_log = LogRepository(MAPPER_PATH)
db_ticket = TicketRepository(MAPPER_PATH)
db_task = TaskRepository(MAPPER_PATH)