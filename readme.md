rest_client 
提供restful api的一切方法实现

order_client 
通过ws提供下单操作的一切方法实现（是否要记录返回的服务端订单id?）

listen_client 
通过ws提供账户信息listen的一切方法实现

order_manager 
实现order类和OrderManager类，实现订单的状态管理和订单的状态更新

account_manager 
实现account类和AccountManager类，实现账户的状态管理（包含初始化）和账户的状态更新

strategy_engine 
不知道，还没想好，可能是计算的调用和信号的发出？

message_dispather 
消息分发，listen得到的消息根据类型调用不同manager的方法处理

strategies 
短期内实现一些统计信号的计算

config 
配置文件





