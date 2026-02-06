# 专门负责清洗数据
import json
from datetime import datetime


def process_raw_sku_data(raw_json):
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
    for sku in perform.get("skuList", []):
        is_salable = 1 if sku.get("skuSalable") == "true" else 0
        price_name = sku.get("priceName")
        rows.append({
            "item_id": basic.get("itemId"),
            "project_title": project_title,
            "venue_name": basic.get("venueName"),
            "perform_id": perform.get("performId"),
            "perform_time": perform_time,
            "sku_id": sku.get("skuId"),
            "price_name": price_name,
            "price": float(sku.get("price", 0)),
            "stock_status": is_salable,
            "limit_quantity": int(perform.get("limitQuantity", 4)),
            "sale_start_time": sale_start_time,
            "updated_at": beijing_now
        })
    return rows