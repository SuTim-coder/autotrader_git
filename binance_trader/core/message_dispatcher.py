import asyncio
import json
from binance_trader.modules.order_manager import OrderManager
from binance_trader.modules.account_manager import AccountManager

class MessageDispatcher:
    def __init__(self,message_queue:asyncio.Queue,ordermanager:OrderManager,accountmanager:AccountManager):
        self.message_queue = message_queue
        self.ordermanager = ordermanager
        self.accountmanager = accountmanager
        self._stop_event = asyncio.Event()
    
    async def start(self):
        while not self._stop_event.is_set():
            message = await self.message_queue.get()
            await self._dispatch(message)

    async def _dispatch(self,message:str):
        parsed_message = json.loads(message)
        event_type = parsed_message.get('e')
        if event_type == 'ACCOUNT_UPDATE':
            print("收到 ACCOUNT_UPDATE 消息，暂不处理。")
            self.accountmanager.update_account(parsed_message)
        elif event_type == 'ORDER_TRADE_UPDATE':
            self.ordermanager.update_order(parsed_message)
