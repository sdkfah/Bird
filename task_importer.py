# task_importer.py
import sys
import os

# 确保程序能找到 core 和 data 包
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.db_handler import DBHandler
import pprint


def import_tasks():
    my_orders = [
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "398.00",
            "info": "石磊义410325200205111529|石星义410325200205111545",
            "priority": "二连",
            "bounty": "80",
            "phone": "15355981554"
        },
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "398.00",
            "info": "吕一330204200607021019",
            "priority": "单机",
            "bounty": "80",
            "phone": "15355981554"
        },
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "398.00",
            "info": "徐梦婷411525200004295749",
            "priority": "单机",
            "bounty": "80",
            "phone": "15355981554"
        },
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "598.00",
            "info": "梁静230602197908155724|黄帆310115201011154472",
            "priority": "二连",
            "bounty": "80",
            "phone": "15355981554"
        },
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "398.00",
            "info": "王敏航330185201105081414",
            "priority": "单机",
            "bounty": "80",
            "phone": "15355981554"
        },
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "798.00",
            "info": "金朵310114200607242624",
            "priority": "包厢",
            "bounty": "50",
            "phone": "15355981554"
        },
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "398.00",
            "info": "黄仁雪51152720051023032X|黄丹532124200401121320",
            "priority": "二连",
            "bounty": "50",
            "phone": "15355981554"
        },
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "398.00",
            "info": "胡子鑫310108200712047831",
            "priority": "单机",
            "bounty": "80",
            "phone": "15355981554"
        },
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "398.00",
            "info": "毛若霖370883200908031611",
            "priority": "单机",
            "bounty": "80",
            "phone": "15355981554"
        },
        {
            "city": "上海",
            "artist": "郑润泽",
            "date": "2026-03-01",
            "price": "398.00",
            "info": "孙素娟410104200707270041",
            "priority": "单机",
            "bounty": "80",
            "phone": "15355981554"
        }
    ]

    if not my_orders:
        print("[-] 未识别到有效订单，请检查格式。")
        return

    # 3. 调用数据包的处理器存入 MySQL
    db = DBHandler()
    db.insert_parsed_tasks(my_orders)

if __name__ == "__main__":
    import_tasks()
