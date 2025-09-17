import json
import time
import threading
import requests
import websockets
import asyncio
import aiohttp
from typing import Optional

class BinanceAsyncWebSocketClient:
    def __init__(self,api_key:str,api_base_url:str,ws_base_url:str,message_queue:asyncio.Queue):
        self.api_key = api_key
        self.api_base_url = api_base_url
        self.ws_base_url = ws_base_url
        self.listen_key: Optional[str] = None
        self.ws_instance = None
        self._stop_event = asyncio.Event()
        self.message_queue = message_queue

    async def get_listen_key(self):
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_base_url}/fapi/v1/listenKey"
                headers = {'X-MBX-APIKEY': self.api_key}
                async with session.post(url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self.listen_key = data['listenKey']
                    print(f"成功获取新的 ListenKey: {self.listen_key}")
                    return self.listen_key
        except aiohttp.ClientError as e:
            print(f"HTTP 错误或网络错误: {e}")
            return False
        except (json.JSONDecodeError, KeyError) as e:
            print(f"获取 listenKey JSON 解析错误或缺失 'listenKey' 字段: {e}")
            return False

    async def renew_listen_key(self):
        try:
            async with aiohttp.ClientSession() as session:
                url=f"{self.api_base_url}/fapi/v1/listenKey"
                headers={'X-MBX-APIKEY': self.api_key}
                async with session.put(url,headers=headers) as response:
                    data = await response.json()
                    if response.status == 200:
                        print(f"更新listenKey成功: {data}")
                        return True
                    else:
                        print(f"ListenKey 续期失败，状态码: {response.status}, 错误信息: {data.get('msg')}")
                        if data.get('code') == -1125:
                            print("ListenKey 已失效，正在重新获取新的key...")
                            return False
        except aiohttp.ClientError as e:
            print(f"http错误或网络错误: {e}")
            return False
        except Exception as e:
            print(f"更新ListenKey时发生异常: {e}")
            return False
    
    async def connect(self):
        message_task = None
        ping_pong_task = None
        renew_task = None
        listen_key = await self.get_listen_key()
        print(f"获取到的 listenKey: {listen_key}")
        if not listen_key:
            print("获取 listenKey 失败，无法连接 WebSocket")
            return

        ws_url = f"{self.ws_base_url}/ws/{listen_key}"
        print(f"连接的ws_url: {ws_url}")
        try:
            ws = await websockets.connect(ws_url)
            self.ws_instance = ws
            print("WebSocket监听端连接成功")
            message_task = asyncio.create_task(self._receive_messages_task())
            ping_pong_task = asyncio.create_task(self._ping_pong_task())
            renew_listen_key_task = asyncio.create_task(self._renew_listen_key_task())
            await asyncio.gather(message_task, ping_pong_task, renew_listen_key_task)
        except Exception as e:
            print(f"WebSocket监听端连接失败: {e}")
        finally:
            if message_task:
                message_task.cancel()
            if ping_pong_task:
                ping_pong_task.cancel()
            if renew_listen_key_task:
                renew_listen_key_task.cancel()
            await self._close_ws_client()

    async def _close_ws_client(self):
        if self.ws_instance:
            await self.ws_instance.close()
            self.ws_instance = None
            print("WebSocket 客户端已关闭")
    
    async def stop(self):
        print("正在请求停止客户端...")
        self._stop_event.set()

    async def _ping_pong_task(self):
        while not self._stop_event.is_set():
            try:
                await self.ws_instance.ping()
                await asyncio.sleep(170) #true:170
            except websockets.exceptions.ConnectionClosedError:
                print("WebSocket 连接已关闭")
                break
            except Exception as e:
                print(f"WebSocket 心跳失败: {e}")
                break
    
    async def _receive_messages_task(self):
        try:
                async for message in self.ws_instance:
                    await self.message_queue.put(message)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"消息接收任务：连接已关闭: {e}") 

    async def _renew_listen_key_task(self):
        while not self._stop_event.is_set():
            success = await self.renew_listen_key()
            if not success:
                # 如果续期失败，休眠一段时间后重试
                await asyncio.sleep(60)
                continue
            # 续期成功，休眠 55 分钟后再次续期
            print("自动续期任务，下一次续期将在 55 分钟后进行...")
            await asyncio.sleep(55*60) #true:55*60

if __name__ == "__main__":
    from ..config import Config

    async def main():
        client = BinanceAsyncWebSocketClient(
            api_key=Config.TEST_API_KEY,
            api_base_url=Config.REST_URL,
            ws_base_url=Config.WS_LISTEN_URL
        )
        try:
            print("客户端开始运行，将在20秒后自动关闭...")
            # 启动客户端的后台任务
            connect_task = asyncio.create_task(client.connect())
            # 等待20秒
            await asyncio.sleep(20)
        finally:
            await client.stop()
            # 确保 connect_task 能够完成
            await connect_task

    asyncio.run(main())