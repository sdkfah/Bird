# services/monitor_service.py
from loguru import logger
from repository import db_order  # 假设你已经初始化了实例
import time


def start_auto_sniper():
    print("[*] 自动匹配系统已启动...")
    while True:
        # 1. 扫描是否有匹配项
        matches = db_order.get_matchable_orders()

        for task in matches:
            logger.info(f"🔥 发现匹配！艺人: {task['artist']} | 客户: {task['customer_info']}")

            # 2. 这里调用你的 Frida RPC 接口触发手机动作
            # success = rpc_manager.call_buy_function(task['sku_id'], ...)

            # 3. 如果手机端反馈下单成功，则更新数据库
            # db_order.mark_task_success(task['task_id'])

        time.sleep(1)  # 频率可调