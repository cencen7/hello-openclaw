"""
给一个ip，和一个cidr list，找出第一个cidr，覆盖这个ip

followup 是 给一个cidr和一个cidr list，有两种，allow和deny，一个一个看，如果是allow且有重叠的就消去，有deny就返回false，看最后给的cidr能不能被完全消掉

大意就是有一堆 CIDR 格式的 allow/deny 防火墙规则，然后输入是一个 IP address，判断是否能通过，如果能匹配多条规则以第一条为准。
follow-up questions:
what other test cases would you write
what if need to support CIDR as input
what would be the condition of a match
then write pseudo code

Follow up是必须要满足每一条rule，只要有一条不满足就false
需要考虑overlap，要先merge

地里常见的CIDR题，给一个list的rules和ip，格式类似[{"allow", CIDR_1}, {"deny", CIDR_2}]，找第一个匹配的（即在范围内的）
，看是allow还是deny；followup是把ip换成cidr，即代表一段范围，全部被allow的范围覆盖才allow，否则deny

---

给你一个array的cidr(没接触过这个概念的朋友们可以先了解一下这个)，每一个cidr map到一个allow/deny的rule，
和一个target IP address，要找到第一个match的rule是什么；
 followup是如果不是target IP address、而是cidr，应该怎么改

 ---
 https://leetcode.com/problems/ip-to-cidr/description/


基本上要创建 a bit mask for the lowest N bits, do (1 << N) - 1



分享完题目讨论下为什么挂 and 怨气这么大，三哥。有一些奇怪的
2's complement thing that made comparisons f***ed
----
以一个list of CIDR IP的形式，给你一个防火墙
{
"DENY", "255.0.0.8/29"
"ALLOW", "117.145.102.64/30"
}
list里后续的entry如果和前面的有overlap，不会覆盖之前的。
现在再给你一个IP address，让你判断这个IP的status是deny还是allow。
---
店面：高频的ip防火墙IP Firewall，其他帖子里也有提到，注意需要提前练习一下bit operation，然后corner case也有点多。之前看到有人分享用转换成Integer/long的解法但是实测有几个case过不了。
---
Coding 3: IP to CIDR 变种
System Design: 设计file system，支持create dir，list dir，put file， get file etc，如果存的文件特别大如何handle
---
follow up input 从ip 变成cidr。 解法类似range module。他家follow up不用写出来应该也是能过的。
---
每个CIDR支持 Allow，Deny
Follow-up: 如何Scale?
"""