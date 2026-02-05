# core/matcher.py
from data.db_handler import DBHandler

class SniperMatcher:
    def __init__(self):
        self.db = DBHandler()

    def process_inventory(self, project_title, sku_list):
        """
        sku_list: 格式为 [{'price_name': '1280', 'salable': 1}, ...]
        """
        for sku in sku_list:
            if sku['salable'] == 1:
                # 发现有票，立即寻找匹配的红包单
                matches = self.db.find_matching_orders(project_title, sku['price_name'])
                if matches:
                    top_order = matches[0]
                    print(f"\n[Sniper Match!] 🎯项目: {project_title} | 票档: {sku['price_name']}")
                    print(f"👤 实名人: {top_order['customer_info']}")
                    print(f"🧧 红包: {top_order['bounty']} | 📞 电话: {top_order['contact_phone']}")
                    print("-" * 50)