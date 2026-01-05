"""
phone screen问了一个k-v store,需要支持put, delete, 以及过去五分钟内的平均QPS查询

follow up是调整QPS的window size

这是一个 KV store，用来计算 AVG LOAD TIME。



大致是设计一个 in-memory key value store，可以进行 PUT/GET 操作。写一个函数能查询在一定时间内你的 AVG PUT 或 GET 是多少。

比如过去 10 分钟，平均每秒多少 GET，平均每秒多少 PUT。

Design key value class， 需要写四个method: 1. put(string key, string value), 2. get(String key), 3. averagePut(), 4. averageGet() - 过去五分钟put/get 平均call 了的次数。

algorithm 考了 kv store 算 qps， followup 问了求任意时间怎么做（我答了前缀和 + 二分），然后问了是否能牺牲精度来节省空间，回答了将单个timestamp改成一段时间


---
一个map， put and get操作，需要计算这两个操作五分钟的qps

我在写简单的queue版本，面试官打断说这个不scalable 说想牺牲精度换取high throughput

面试官提示可以每秒计算aggregate

我提出可以用一个300的array，写完了put操作并且跑了几个我写的test。

但我每次操作的时候都重新扫+assign一遍这个array很不优雅，然后分析复杂度是 O 300

面试官提出可以更优化，这个时候时间不多了我又绕回了queue还没有写出来

面试结束后才想明白可以取模 % 更新

---
Hashmap QPS. 不要求thread safe，很多followup，比如高效查询不止最近5分钟的hit count，要最近24小时之类的，讨论使用不同数据结构实现的tradeoffs

----
durable KV store, 印度staff manager迟到十多分钟， 首先质疑我为啥懂wal， 然后我做任何改动都质疑一下，前半部分不准我想任何多线程解决方案，浪费很多时间，以至于最后加锁部分简单写了， 无锁concurrency部分只能口述，我说了乐观锁， 然后feedback ：concurency部分code写少了。
"""