class Config:
    """交易系统的所有配置信息。"""

    # --- Binance API 配置 ---
    TEST_API_KEY = "your key"
    TEST_API_SECRET = "your secret"
    # 主网
    API_KEY = "your key"
    
    # --- REST API URL ---
    # 测试网
    REST_URL = 'https://testnet.binancefuture.com'
    # 主网
    # REST_URL = 'https://fapi.binance.com'

    # --- WebSocket URL ---
    # 主网
    WS_LISTEN_URL = 'wss://fstream.binance.com'

    # 测试网 下单url
    WS_ORDER_URL = 'wss://testnet.binancefuture.com/ws-fapi/v1'

    # --- WebSocket 配置 ---
    LISTENKEY_VALIDITY_MINUTES = 60
    LISTENKEY_EXTEND_INTERVAL_SECONDS = LISTENKEY_VALIDITY_MINUTES * 60 // 2
    MAX_RETRIES = 10
