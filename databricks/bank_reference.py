"""
Bank Reference
NewAccount(credit) method会给每个 user 新建一个 account，返回 accountId
NewAccount(credit, refId) ，新建 account 的时候指定一个推荐人 id, 那么这个推荐人也获得相同的 credit
例如 A credit = 300, A refer 了 b, b credit = 200，那么 a credit 变成 500
第一问是求 credit 不小于一个 number 的 TopK
Followup 是如果间接 refer 也算 credit 怎么处理。例如 a refer b, b refer c, c's credit should be add to both a & b.
System Programming: Log Writer.
很多个线程同时写，实现这个 write method.要求是 write 要在确保数据 persist 到 disk 上后才 return。
Arch: 股票交易。
用户可以提交一个想要交易的价格 和一个 timeout 时间，需要在 timeout 结束之前完成交易，如果到时间没有成功交易那么 cancel 这个交易。
"""