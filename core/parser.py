# core/parser.py



class SmartParser:
    @staticmethod
    def parse_text():
        # 2. 准备你的业务数据 (直接按你提供的格式录入)
        # my_orders = [
        #     {
        #         'keyword': '',
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
                'keyword': '谢霆锋深圳',
                'date': '3月21',
                'price': '980看台',
                'info': '陈满林 442000198207285710 | 区锦暖 442000198103305705',
                'priority': '二连',
                'bounty': 350,
                'phone': '15355981554'
            },
            {
                'keyword': '谢霆锋深圳',
                'date': '3月21',
                'price': '980看台',
                'info': '黄仕娇 441422197906164023 | 张丹凤 441423198711066029',
                'priority': '二连',
                'bounty': 350,
                'phone': '15355981554'
            },
            {
                'keyword': '谢霆锋深圳',
                'date': '3月21',
                'price': '980看台',
                'info': '张文斌 44078319950522781X',
                'priority': '单机',
                'bounty': 300,
                'phone': '15355981554'
            },
            {
                'keyword': '谢霆锋深圳',
                'date': '3月21',
                'price': '980看台',
                'info': '胡强 440307198204181114 | 黎琼英 42108319860221242X',
                'priority': '二连',
                'bounty': 350,
                'phone': '15355981554'
            }
        ]
        return my_orders