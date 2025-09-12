import json
import time
import threading
import requests
import websockets
import asyncio
import aiohttp

class BinanceAsyncWebSocketClient:
    def __init__(self,api_key,api_base_url,ws_base_url):
        self.api_key = api_key
        self.api_base_url = api_base_url
        self.ws_base_url = ws_base_url
        self.listen_key = None
        self.ws_instance = None
        self.ws_thread = None
        self.listen_key_thread = None
        self.reconnect_lock = threading.Lock()
        self.should_reconnect = True

    async def get_listen_key(self):
        if self.listen_key:
            return self.listen_key
        else:
            try:
                async with aiohttp.ClientSession() as session:
                    url=f"{self.api_base_url}/fapi/v1/listenKey"
                    headers={'X-MBX-APIKEY': self.api_key}
                    async with session.post(url,headers=headers) as response:
                        response.raise_for_status()
                        data = await response.json()
                        self.listen_key = data['listenKey']
                        return self.listen_key
            except aiohttp.ClientError as e:
                print(f"http错误或网络错误: {e}")
                return None
            except (json.JSONDecodeError, KeyError) as e:
                print(f"获取listenKey JSON 解析错误或缺失 'listenKey' 字段: {e}")
                return None
    
    async def connect(self):
        listen_key = await self.get_listen_key()
        print(f"获取到的 listenKey: {listen_key}")
        if not listen_key:
            print("获取 listenKey 失败，无法连接 WebSocket")
            return

        ws_url = f"{self.ws_base_url}/ws/{listen_key}"
        try:
            async with websockets.connect(ws_url) as ws:
                self.ws_instance = ws
                print("WebSocket监听端连接成功")
                message_task = asyncio.create_task(self._receive_messages())
                ping_pong_task = asyncio.create_task(self._ping_pong_task())
                await asyncio.gather(message_task, ping_pong_task)
        except Exception as e:
            print(f"WebSocket监听端连接失败: {e}")  

    async def _ping_pong_task(self):
        while self.ws_instance:
            try:
                await self.ws_instance.ping()
                await asyncio.sleep(10)
            except websockets.exceptions.ConnectionClosedError:
                print("WebSocket 连接已关闭")
                break
            except Exception as e:
                print(f"WebSocket 心跳失败: {e}")
                break
    
    async def _receive_messages(self):
        try:
                async for message in self.ws_instance:
                    print(f"收到消息: {message}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"消息接收任务：连接已关闭: {e}") 


if __name__ == "__main__":
    from ..config import Config

    async def main():
    # 创建一个 WebSocket 客户端实例
        client = BinanceAsyncWebSocketClient(
            api_key=Config.TEST_API_KEY,
            api_base_url=Config.REST_URL,
            ws_base_url=Config.WS_LISTEN_URL
        )
        await client.connect()

    asyncio.run(main())