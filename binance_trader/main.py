import sys
import os
import datetime
from copy import deepcopy  # 导入 deepcopy，用于更深入的测试

# 将项目根目录添加到 Python 的搜索路径中，以便能够找到 binance_trader 包
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 现在可以正常导入 Order 和 OrderManager 类了
from binance_trader.models.order import Order
from binance_trader.managers.order_manager import OrderManager

def test_get_all_orders():
    """
    测试 OrderManager.get_all_orders() 方法。
    验证它是否返回一个订单字典的副本，并且修改副本不会影响原始数据。
    """
    print("\n--- 正在运行测试: test_get_all_orders ---")
    
    # 1. 创建 OrderManager 实例
    manager = OrderManager()

    # 2. 创建并添加几个 Order 实例
    order1 = Order(client_order_id="test_id_1", symbol="BTCUSDT", side="BUY", price=60000.0, quantity=1.0, order_type="LIMIT")
    order2 = Order(client_order_id="test_id_2", symbol="ETHUSDT", side="SELL", price=3000.0, quantity=2.0, order_type="MARKET")
    
    manager.create_order(order1)
    manager.create_order(order2)

    # 3. 调用 get_all_orders() 获取所有订单
    retrieved_orders = manager.get_all_orders()

    # 4. 验证：检查返回的字典是否是副本
    # 使用 'is' 关键字检查两个对象是否是同一个
    assert retrieved_orders is not manager.orders
    print("✅ 验证通过: 返回的字典是原始字典的一个副本。")

    # 5. 验证：检查字典内容是否一致
    assert len(retrieved_orders) == 2
    
    # 移除 assert retrieved_orders.get("test_id_1") is manager.orders.get("test_id_1")
    # 因为我们现在使用的是深拷贝，这两个对象不再是同一个，这个断言会失败。
    # 我们可以通过比较属性来验证内容是否一致。
    assert retrieved_orders.get("test_id_1").client_order_id == manager.orders.get("test_id_1").client_order_id
    assert retrieved_orders.get("test_id_1").symbol == manager.orders.get("test_id_1").symbol
    print("✅ 验证通过: 字典的长度和内容都正确。")

    # 6. 验证：修改副本，并检查原始字典是否受到影响
    # 模拟修改副本中的一个订单的状态
    retrieved_orders["test_id_1"].status = "CANCELED"
    
    # 检查原始字典中，同一个订单的状态是否未被修改
    assert manager.orders["test_id_1"].status != "CANCELED"
    print("✅ 验证通过: 修改副本中的订单，不会影响原始订单。")

    # --- 新增步骤：测试订单状态更新后，副本是否正确 ---
    print("\n--- 正在测试订单状态更新对 get_all_orders() 的影响 ---")

    # 模拟一个来自交易所的订单状态更新数据
    mock_update_data = {
      "e":"ORDER_TRADE_UPDATE",
      "E":1568879465651,
      "T":1568879465650,
      "o":{
        "s":"BTCUSDT",
        "c": "test_id_1",
        "X":"PARTIALLY_FILLED",
        "i":987654321,
        "z":"0.5",
        "ap":"60000.0",
        "L":"60000.0",
        "q":"1.0"
      }
    }
    
    # 调用 update_order 方法更新原始订单
    manager.update_order(mock_update_data)
    
    # 再次调用 get_all_orders() 获取新的副本
    new_retrieved_orders = manager.get_all_orders()
    
    # 检查新副本中的订单状态是否已被正确更新
    assert new_retrieved_orders["test_id_1"].status == "PARTIALLY_FILLED"
    print("✅ 验证通过: 新的副本正确反映了订单的最新状态。")

    print("\n--- 所有测试通过！get_all_orders() 方法功能正常。---")

# 运行测试
if __name__ == "__main__":
    test_get_all_orders()
