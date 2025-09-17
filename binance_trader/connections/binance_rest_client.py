import aiohttp
import hmac
import hashlib
from urllib.parse import urlencode
import time
from typing import Dict, Any
import asyncio

class BinanceRestClient:
# 异步的REST API客户端，用于签名和request，需要传入key,secret,base_url
# 目前已实现：通过get_account_info方法实现账户信息获取
# 待完善：get_account_info方法应当调用一个过滤0持仓的内部方法
# 待完善：改写逻辑，用try except实现鲁棒性
# 待完善：通过restful接口下单，查询订单等功能
    def __init__(self,api_key,api_secret,base_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = aiohttp.ClientSession()
    
    async def close_client(self):
        await self.session.close()
    
    def _generate_signature(self,params: Dict[str, Any]):
        signed_params = params.copy()
        signed_params['timestamp'] = int(time.time() * 1000)
        sorted_keys = sorted(signed_params.keys())
        query_string_list = []
        for key in sorted_keys:
            value = signed_params[key]
            query_string_list.append(f"{key}={value}")
        query_string = "&".join(query_string_list)
        api_key_bytes = self.api_secret.encode('utf-8')
        query_string_bytes = query_string.encode('utf-8')
        signature = hmac.new(api_key_bytes, query_string_bytes, hashlib.sha256).hexdigest()
        signed_params['signature'] = signature
        return signed_params
    
    async def _send_signed_request(self,http_method:str,endpoint:str,params:dict):
        params_signature = self._generate_signature(params)
        query_string = urlencode(params_signature)
        url = f"{self.base_url}{endpoint}?{query_string}"
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        print("URL:", url)
        print("Headers:", headers)
        print("Params:", params_signature)
        async with self.session.request(http_method,url,headers=headers) as response:
            response.raise_for_status()
            return await response.json()
        
    async def get_account_info(self):
        endpoint = "/fapi/v2/account"
        params = {}
        return await self._send_signed_request("GET",endpoint,params)


async def main():
    from ..config import Config

    print(Config.TEST_API_KEY)
    print(Config.TEST_API_SECRET)
    print(Config.REST_URL)

    # 实例化客户端
    client = BinanceRestClient(
            api_key=Config.TEST_API_KEY,
            api_secret=Config.TEST_API_SECRET,
            base_url=Config.REST_URL
        )
    

    try:
        print("尝试获取账户信息...")
        account_info = await client.get_account_info()
        print("成功获取账户信息：")
        print(account_info)
    except aiohttp.ClientResponseError as e:
        print(f"API 请求失败：{e.status} - {e.message}")
        print("请检查你的 API Key 和 Secret，以及网络连接。")
    except Exception as e:
        print(f"发生未知错误：{e}")
    finally:
        # 确保在程序结束时关闭会话
        await client.close_client()

if __name__ == "__main__":
    asyncio.run(main())
