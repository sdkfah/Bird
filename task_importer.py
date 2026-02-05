# task_importer.py
import sys
import os

# 确保程序能找到 core 和 data 包
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.parser import SmartParser
from data.db_handler import DBHandler
import pprint


def import_tasks():

    print("[*] 正在解析报单文本...")

    # 2. 调用核心包的解析器
    parser = SmartParser()
    tasks = parser.parse_text()
    if not tasks:
        print("[-] 未识别到有效订单，请检查格式。")
        return

    pprint.pprint(tasks)

    # 3. 调用数据包的处理器存入 MySQL
    db = DBHandler()
    db.insert_parsed_tasks(tasks)

if __name__ == "__main__":
    import_tasks()