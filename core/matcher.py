# core/matcher.py
import json
import os
import re

from data.db_handler import DBHandler


class SniperMatcher:
    def __init__(self):
        self.db = DBHandler()

    def show_task_dashboard(self, artist_name=None):
        # 调用关联查询方法
        matches = self.db.get_matched_tasks_report(artist_name)

        # ANSI 颜色配置
        C = "\033[96m"  # 青色
        G = "\033[92m"  # 绿色
        Y = "\033[93m"  # 黄色
        R = "\033[91m"  # 红色
        M = "\033[95m"  # 洋红色
        W = "\033[0m"  # 重置

        title = f" 🎯 狙击手实时匹配看板 ({artist_name if artist_name else '全量视角'}) "
        print(f"\n{C}{title:=^160}{W}")

        # 重新设计的表头：实名人与顺序完全独立
        header = (f"{'ID':<4} | {'红包':<8} | {'艺人':<8} | {'匹配票档':<18} | "
                  f"{'状态':<4} | {'SKU_ID':<18} | {'场次ID':<12} | {'优先顺序':<10} | {'实名人信息 (完整)'}")
        print(f"{Y}{header}{W}")
        print("-" * 165)

        if not matches:
            print(f"{R}{' [!] 暂无匹配任务：请检查库存数据或任务日期格式':^160}{W}")
        else:
            for m in matches:
                # 状态美化
                status = f"{G}✅有{W}" if m['has_stock'] == 1 else f"{R}❌无{W}"

                # 字段提取与对齐
                t_id = f"{M}{m['task_id']:<4}{W}"
                bounty = f"{Y}{float(m['bounty']):>8.2f}{W}"
                artist = f"{m['artist']:<10}"
                price_tag = f"{m['price_tag']:<20}"
                sku_id = f"{m['sku_id']:<20}"
                perform_id = f"{m['perform_id']:<14}"
                priority = f"{m['priority_order'] if m['priority_order'] else '默认':<12}"

                # 实名人信息：完全保留，不进行切片省略
                customer_full = m['customer']

                line = (
                    f"{t_id} | {bounty} | {artist} | {price_tag} | {status} | "
                    f"{sku_id} | {perform_id} | {priority} | {customer_full}"
                )
                print(line)

        print(f"{C}{'=' * 165}{W}\n")
        return matches  # 优化点：返回结果集

    def deploy_to_protocol(self, target):
        """构造 KV 格式配置并推送到手机"""
        if not target:
            print("[-] 目标数据为空，取消推送")
            return

        # 1. 解析实名人信息为字典 {姓名: 身份证}
        # 匹配中文姓名 + 18位身份证
        pairs = re.findall(r'([\u4e00-\u9fa5]+)(\d{17}[\dXx])', target['customer'])
        viewer_dict = {name: id_card for name, id_card in pairs}
        count = len(viewer_dict) if viewer_dict else 1

        # 2. 构造你要求的 JSON 格式
        # buy_param 格式: 项目ID_数量_SKUID
        item_id = str(target['item_id'])
        sku_id = str(target['sku_id'])

        protocol_config = {
            "item_id": item_id,
            "sku_id": sku_id,
            "buy_param": f"{item_id}_{count}_{sku_id}",
            "viewers": viewer_dict,
            "task_settings": {
                "interval_ms": 50
            }
        }

        # 3. 写入并推送
        config_path = "config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(protocol_config, f, ensure_ascii=False, indent=4)

        # 推送到 Frida 脚本监听的目录
        os.system(f"adb push {config_path} /data/local/tmp/config.json")
        print(f"\n\033[92m[+] 任务 {target['task_id']} 已按照新格式推送成功！\033[0m")
        print(f"    - 数量: {count} | 实名人: {list(viewer_dict.keys())}")
if __name__ == "__main__":
    matcher = SniperMatcher()

    # 1. 获取并展示数据 (仅查询一次 DB)
    all_matches = matcher.show_task_dashboard('乒联乒联')

    # 2. 内存查找 ID 为 44 的任务并推送
    task_44 = next((m for m in all_matches if m['task_id'] == 44), None)
    if task_44:matcher.deploy_to_protocol(task_44)