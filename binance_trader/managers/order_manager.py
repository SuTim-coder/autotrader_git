import datetime
from copy import deepcopy

class OrderManager:
    def __init__(self):
        self.orders = {}

    def create_order(self,order_obj):
        if order_obj.client_order_id in self.orders:
            print(f"订单ID {order_obj.client_order_id} 已存在")
            return None

        self.orders[order_obj.client_order_id] = order_obj
        print(f"订单ID {order_obj.client_order_id} 创建成功")

    def update_order(self,data):
        order_info = data.get('o')
        if not order_info:
            print("警告：收到的数据格式不正确，缺少 'o' 字段。")
            return
        
        client_order_id = order_info.get('c')
        if not client_order_id:
            print("警告：收到的订单更新缺少客户端ID，已忽略。")
            return
        
        if client_order_id not in self.orders:
            print(f"警告：收到未知订单 {client_order_id} 的更新，已忽略。")
            return
        
        order = self.orders[client_order_id]

        order.status = order_info.get('X')  # 订单状态
        order.filled_quantity = float(order_info.get('z', 0))  # 累计成交量
        order.avg_fill_price = float(order_info.get('ap', 0))  # 平均成交价格
        order.update_time = datetime.datetime.now()  # 使用本地时间

        exchange_order_id = order_info.get('i')
        if exchange_order_id and not order.exchange_order_id:
            order.exchange_order_id = exchange_order_id
        print(f"订单 {client_order_id} 已更新，当前状态: {order.status}，已成交量: {order.filled_quantity}")
    
    def get_all_orders(self):
        return deepcopy(self.orders)
