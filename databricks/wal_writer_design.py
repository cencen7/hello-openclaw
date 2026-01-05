"""
Design WAL writer, 
single machine, highest throughput, 
log is durablely written before the call returns to caller.

Coding 2 (multi-thread): 
设计single machine， multi-client chat system，
一个user 可以subscribe 好几个channel，user往channel里发消息的时候所有subscribe的user都会收到消息
"""