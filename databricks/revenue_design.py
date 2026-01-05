"""
databrick revenue 系统
insert(revenue: int, referrer: Optional[int]) -> int 
新增客户并返回自增 id（0 开始）。referrer 如不为空，表示“i 被 referrer 直接推荐”，
因此 referrer 的总收入会增加 revenue。
 get_lowest_k_by_total_revenue(k: int, min_total_revenue: int) -> Set[int] 
 在所有 total_revenue(i) ≥ min_total_revenue 的客户中，
 按 total_revenue 升序（同分按 id 升序）取前 k 个 id，返回集合。
 记住：total_revenue(i) = revenue + sum(revenue[ch] for ch in children)，只一层。

最后还有follow up 如何实时top - k


---
地里出现过的Revenue System，需要实现add，addByReferral和getTopKCustomer(minRevenue)
首先需要一个Customer class with id and totalRevenue
Write heavy: 两个add的时候直接放入Hashmap，然后get的时候用一个minHeap遍历就可以，add是O(1)，get是O(nlogk)
Read heavy/Read-Write Balance: 维护一个SortedSet(我用的是Java)，然后add的时候放入Map和Set，addByReferral的时候先add new customer，然后把referrer从set拿出来，加上revenue再放回去。get的时候用set iterator或者for each loop直接找前k个满足条件就行，add是O(logn)，get是O(k)
Follow up: 给一个Customer id，然后找到所有这个id向下关联的id，根据refer level划分。比如
a refer b, a refer c
b refer d, c refer f
f refer h
Then getRelation(a) should return {{b, c}, {d, f}, {h}}
用一个map存id和它refer的id list，把refer关系抽象为有向图，然后从root id开始做bfs就行，跟leetcode那些course schedule的题有点像
----
Design a payment gateway system. You will support multiple types of credit cards or bank cards. Consider your clients will have pos machines to scan the card and call your API to submit payment.

Your scope is just design the card validation part not the full transaction. It has high availability and latency requirement.

Based on card number, how to route to the bank endpoint.

Design the api schema for both gateway APIs and bank APIs.

How to handle failures?

Estimate the server loads.
---
insert(revenue): 返回一个auto-increment的customer id
insert(revenue, referrer): 返回一个auto-increment的customer id，和1的不同是这个新的customer是被referrer refer的
get_top_k_revenue(k, min_revenue) -> set[int]: 返回有topk revenue的customer，但是要满足revenue 不小于min_revenue。每个customer的revenue是自己的revenue和被他直接refer的customer的revenue总和。
"""