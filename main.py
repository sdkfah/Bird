from core.frida_manager import FridaManager
from services.data_processor import process_raw_sku_data
from repository import db_ticket  # 预先实例化的 TicketRepository


def global_on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        if payload.get('type') == 'SKU_DATA':
            # 1. 业务层清洗
            rows = process_raw_sku_data(payload.get('data'))
            # 2. 仓库层持久化
            db_ticket.batch_upsert_skus(rows)


if __name__ == "__main__":
    # 未来这里可以从数据库读取所有“在线”设备的 SN，循环启动
    sn_list = ["SN_PHONE_01", "SN_PHONE_02"]
    for sn in sn_list:
        manager = FridaManager(sn)
        manager.run_agent(global_on_message)

    import sys

    sys.stdin.read()