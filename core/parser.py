# core/parser.py



class SmartParser:
    @staticmethod
    def parse_text():
        # 2. 准备你的业务数据 (直接按你提供的格式录入)
        # my_orders = [
        #     {
        #         'city': '',
        #         'artist':'',
        #         'date': '', #
        #         'price': '',
        #         'info': '',
        #         'priority': '',
        #         'bounty': 0,
        #         'phone': ''
        #     }
        # ]

        my_orders = [
            {
                "city": "深圳",
                "artist": "谢霆锋",
                "date": "2026-03-21",
                "price": "980.00",
                "info": "陈满林442000198207285710|区锦暖442000198103305705",
                "priority": "二连",
                "bounty": "350",
                "phone": "15355981554"
            },
            {
                "city": "深圳",
                "artist": "谢霆锋",
                "date": "2026-03-21",
                "price": "980.00",
                "info": "黄仕娇441422197906164023|张丹凤441423198711066029",
                "priority": "二连",
                "bounty": "350",
                "phone": "15355981554"
            },
            {
                "city": "深圳",
                "artist": "谢霆锋",
                "date": "2026-03-21",
                "price": "980.00",
                "info": "张文斌44078319950522781X",
                "priority": "单机",
                "bounty": "300",
                "phone": "15355981554"
            },
            {
                "city": "深圳",
                "artist": "谢霆锋",
                "date": "2026-03-21",
                "price": "980.00",
                "info": "胡强440307198204181114|黎琼英42108319860221242X",
                "priority": "二连",
                "bounty": "350",
                "phone": "15355981554"
            }
        ]
        return my_orders