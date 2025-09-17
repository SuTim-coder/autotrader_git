rest_client 提供restful api的一切方法实现
order_client 通过ws提供下单操作的一切方法实现（是否要记录返回的服务端订单id?）
listen_client 通过ws提供账户信息listen的一切方法实现

order_manager 实现order类和OrderManager类，实现订单的状态管理和订单的状态更新
account_manager 实现account类和AccountManager类，实现账户的状态管理（包含初始化）和账户的状态更新
strategy_engine 不知道，还没想好，可能是计算的调用和信号的发出？

message_dispather 消息分发，listen得到的消息根据类型调用不同manager的方法处理

strategies 短期内实现一些统计信号的计算

config 配置文件





---
config:
  look: handDrawn
---
flowchart TD
    subgraph S1[数据源层]
        ExternalDataSource[外部数据源]
        BinanceServer(Binance服务器)
    end
    subgraph S2[客户端层]
        DataCollector[数据采集模块]
        BinanceClient[Binance客户端]
    end
    subgraph S3[服务层]
        DataManager[数据管理器]
        MessageDispatcher{消息分发器}
        RiskManager[风控模块]
    end
    subgraph S4[核心业务层]
        StrategyEngine[策略引擎]
        OrderManager[订单管理器]
        AccountManager[账户管理器]
        DatabaseClient[数据库客户端]
        Database[(数据库)]
        Frontend[前端界面]
    end
    ExternalDataSource -- 实时数据 --> DataCollector
    BinanceServer -- 实时数据流 & 响应 --> BinanceClient
    DataCollector -- 统一格式数据 --> DataManager
    BinanceClient -- 实时数据流 --> MessageDispatcher
    MessageDispatcher -- 广播订单/账户更新 --> OrderManager & AccountManager
    MessageDispatcher -- 广播账户/仓位数据 --> RiskManager
    DataManager -- 提供历史数据 --> StrategyEngine
    StrategyEngine -- 下单指令 --> OrderManager
    StrategyEngine -- 查询 --> AccountManager
    OrderManager -- 下单/取消指令 --> BinanceClient
    OrderManager -- 持久化数据 --> DatabaseClient
    AccountManager -- 查询账户状态 --> BinanceClient
    AccountManager -- 持久化数据 --> DatabaseClient
    DatabaseClient -- 读写 --> Database
    Frontend -- 查询数据 --> OrderManager & AccountManager
    RiskManager -- 紧急平仓/撤单(强制指令) --> BinanceClient
    classDef layerFill fill:#f9f9f9,stroke:#333;
    class S1,S2,S3,S4 layerFill;
    classDef clientStyle fill:#cceeff,stroke:#66aaff,stroke-width:2px;
    class BinanceClient,DataCollector,DatabaseClient clientStyle;
    classDef managerStyle fill:#d9ffcc,stroke:#66aaff,stroke-width:2px;
    class OrderManager,AccountManager,DataManager managerStyle;
    classDef coreStyle fill:#ffcc99,stroke:#66aaff,stroke-width:2px;
    class StrategyEngine coreStyle;
    classDef riskStyle fill:#ffcccc,stroke:#ff6666,stroke-width:3px;
    class RiskManager riskStyle;
    classDef dbStyle fill:#ffccff,stroke:#cc99cc;
    class Database dbStyle;
