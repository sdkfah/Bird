# services/match_service.py

from repository import db_order


def auto_match_and_run():
    # 1. 找出现在有票且符合订单任务的项目
    tasks = db_order.get_matchable_orders()

    for task in tasks:
        # 2. 调用核心层的 RPC 或 ADB 下发抢票指令
        print(f"发现匹配！正在为 {task['customer_info']} 抢购 SKU: {task['sku_id']}")
