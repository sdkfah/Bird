# items_import.py
import frida
import json
import sys
from datetime import datetime
from data.db_handler import DBHandler
from core.matcher import SniperMatcher

# 初始化组件
db = DBHandler()
matcher = SniperMatcher()


def on_message(message, data):
    if message['type'] == 'send':
        payload = message['payload']
        if payload.get('type') == 'SKU_DATA':
            handle_sku_data(payload.get('data'))


def handle_sku_data(raw_json):
    try:
        data = json.loads(raw_json)
        basic = data.get("itemBasicInfo", {})
        perform = data.get("perform", {})
        project_title = basic.get("projectTitle")

        # --- 核心修复：由 Python 统一定义北京时间 ---
        # 即使服务器在海外，datetime.now() 也会获取你运行脚本的电脑本地时间
        beijing_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 预处理时间格式
        fmt = "%Y-%m-%d %H:%M:%S"
        raw_s_time = basic.get("sellingStartTime", "")
        raw_p_time = perform.get("performBeginDTStr", "")
        sale_start_time = datetime.strptime(raw_s_time, "%Y%m%d%H%M").strftime(fmt) if raw_s_time else None
        perform_time = datetime.strptime(raw_p_time, "%Y%m%d%H%M").strftime(fmt) if raw_p_time else None

        rows = []
        sku_status_list = []

        for sku in perform.get("skuList", []):
            is_salable = 1 if sku.get("skuSalable") == "true" else 0
            price_name=sku.get("priceName")
            rows.append((
                basic.get("itemId"),
                project_title,
                basic.get("venueName"),
                perform.get("performId"),
                perform_time,
                sku.get("skuId"),
                price_name,
                float(sku.get("price", 0)),
                is_salable,
                int(perform.get("limitQuantity", 4)),
                sale_start_time,
                beijing_now
            ))
            sku_status_list.append({'price_name': price_name, 'salable': is_salable})

        db.upsert_ticket_items(rows)

    except Exception as e:
        print(f"[-] 数据处理异常: {e}")


def main():
    db.init_tables()  # 确保表结构存在
    try:
        device = frida.get_usb_device()
        session = device.attach("大麦")

        with open("bridge/agent.js", "r", encoding="utf-8") as f:
            script = session.create_script(f.read())

        script.on('message', on_message)
        script.load()
        print("[*] Bird Sniper 系统已启动，正在监听库存...")
        sys.stdin.read()
    except Exception as e:
        print(f"[-] 启动失败: {e}")


if __name__ == "__main__":
    main()