"""
https://stackoverflow.com/questions/75431526/create-a-space-efficient-snapshot-set

除了基本的 set 功能，还需要支持快照（snapshot）特性：
在任意时刻，客户端可以基于当前集合创建一个迭代器（iterator）。
该迭代器只能读取创建时的快照内容，不受之后集合更新（add/remove）的影响。
该迭代器完全iterate后才会继续创建下一个迭代器

功能说明
add(x)

：向集合添加元素 x。
remove(x)

：从集合移除元素 x。
iterator()

：返回一个只读当前快照内容的迭代器。

示例ss = SnapshotSet([1, 2, 3]) # 初始集合为 {1, 2, 3}
ss.add(4) # 集合变为 {1, 2, 3, 4}
iter1 = ss.iterator() # 创建快照迭代器，内容为 {1, 2, 3, 4}
print(iter1.next()) # 输出: 1
print(iter1.next()) # 输出: 2
ss.remove(3) # 集合变为 {1, 2, 4}
print(iter1.next()) # 输出: 3
iter2 = ss.iterator() # 创建快照迭代器，内容为 {1, 2, 4}
ss.add(6) # 集合变为 {1, 2, 4, 6}
print(iter2.next()) # 输出: 1
额外说明
其实这个题目实际运行中是有问题的, 如果用dictionary无法避免key 的add/delete, 在iterate 过程中一定会报错。所以这个题更像假设该情况下，如何implement
-----

题目是要求实现一个 SnapshotSet, iterator 创建时 freeze 这个iter的内容，但是本身set contains 的返回值需要与时俱进.

我一开始搞错了题目（没仔细读样例，大家引以为戒），我以为是iterator 跑的时候就需要iterator update 内容，于是开始说 binary search tree, balance tree 这种东西。
不过面试官还是不错的，帮我扳回来了。

然后就问，single thread / multi-thread, 多少个iterator的问题了，说从single thread, single iterator开始。
方法是对增加删除做个标记，这个写了一下代码。

然后就是问到多个 iterator 如何做标记，我说引入timestamp，需要对iterator和他们的创建时间进行管理，这里会有一些算法用到，等等。
这个时候时间已经不多了，我就简化了具体算法方面的讨论。
没有讨论 multi-thread 的情况，multi-thread本身是一个复杂得多的问题，我猜测也不是要求的。

---

Coding 2 (multi-thread): 
设计single machine， multi-client chat system，
一个user 可以subscribe 好几个channel，user往channel里发消息的时候所有subscribe的user都会收到消息
"""