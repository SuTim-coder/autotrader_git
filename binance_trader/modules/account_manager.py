from typing import Dict, Any

class AccountManager:
    def __init__(self):
        print("临时 AccountManager 已创建。")
    
    def update_account(self, data):
        # 临时占位符，不执行任何操作
        print(f"临时 AccountManager 收到账户更新消息，暂不处理。")
        pass

class Account:
    def __init__(self):
        self.balance:Dict[str,Any] = {}
        self.position:Dict[str,Any] = {}
        
