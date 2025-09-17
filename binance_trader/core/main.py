import asyncio
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from binance_trader.connections.binance_listen_client import BinanceAsyncWebSocketClient
from binance_trader.core.message_dispatcher import MessageDispatcher
from binance_trader.modules.order_manager import OrderManager
from binance_trader.modules.account_manager import AccountManager  
from binance_trader.config import Config

async def main():
    print("--- 正在启动交易机器人主程序 ---")
    
    # 1. 创建所有核心组件的实例
    message_queue = asyncio.Queue()
    order_manager = OrderManager()
    account_manager = AccountManager()
    
    # 2. 创建 WebSocket 客户端实例并传递队列
    # 请替换为你的实际 API 和 Secret Key
    binance_listener_ws_client = BinanceAsyncWebSocketClient(
        api_key=Config.TEST_API_KEY,
        api_base_url=Config.REST_URL,
        ws_base_url=Config.WS_LISTEN_URL,
        message_queue=message_queue
    )
    
    # 3. 创建消息分发器实例，并将所有组件连接起来
    message_dispatcher = MessageDispatcher(
        message_queue=message_queue,
        ordermanager=order_manager,
        accountmanager=account_manager
    )

    # 4. 使用 asyncio.gather() 并发启动所有需要持续运行的任务
    # 然后使用 asyncio.wait_for() 确保程序在60秒后超时并退出
    try:
        print("程序将在120秒后自动结束，您也可以按 Ctrl+C 提前退出。")
        await asyncio.wait_for(
            asyncio.gather(
                binance_listener_ws_client.connect(),
                message_dispatcher.start()
            ),
            timeout=120.0
        )
    except asyncio.TimeoutError:
        print("\n--- 程序因超时（120秒）自动结束。---")
    except KeyboardInterrupt:
        print("\n--- 程序被用户手动中断。---")
    finally:
        print("主程序已退出。")

if __name__ == "__main__":
    asyncio.run(main())
