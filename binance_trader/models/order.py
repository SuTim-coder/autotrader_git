import datetime

class Order:
    def __init__(self,
                 client_order_id,
                 symbol,
                 side,
                 price,
                 quantity,order_type):
        self.client_order_id = client_order_id
        self.exchange_order_id = None
        self.symbol = symbol
        self.side = side
        self.price = price
        self.quantity = quantity
        self.order_type = order_type
        self.status = "PLACING"
        self.create_time = datetime.datetime.now()
        self.update_time = datetime.datetime.now()
        self.filled_quantity = 0.0
        self.avg_fill_price = 0.0

    def __repr__(self):
        """
        这个方法让你能以一种易读的方式打印 Order 对象
        """
        return (f"Order(ID={self.client_order_id}, "
                f"Symbol={self.symbol}, "
                f"Side={self.side}, "
                f"Status={self.status}, "
                f"Filled={self.filled_quantity}/{self.quantity})")
