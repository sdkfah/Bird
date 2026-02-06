from core.frida_manager import FridaManager
from services.data_processor import process_raw_sku_data
from repository import db_log

def global_on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        db_log.info(sn, f"收到数据上报: {payload.get('type')}", module="Frida")

        if payload.get('type') == 'SKU_DATA':
            try:
                process_raw_sku_data(payload.get('data'))
            except Exception as e:
                # 记录错误到数据库
                db_log.error(sn, f"处理失败: {str(e)}", module="Processor")


if __name__ == "__main__":
    # 未来这里可以从数据库读取所有“在线”设备的 SN，循环启动
    sn_list = ["SN_PHONE_01", "SN_PHONE_02"]
    for sn in sn_list:
        manager = FridaManager(sn)
        manager.run_agent(global_on_message)

    import sys

    sys.stdin.read()