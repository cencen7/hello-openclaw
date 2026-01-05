"""
Fibonacci Tree

这道题 algorithm - Finding a path between two nodes in a k-th order fibonacci tree - Stack Overflow
解法跟上面链接里高赞答案那个差不多；
核心思路就是 fibonacci 树的大小可以直接根据 order 计算出来，所以可以不用建树直接在原数组上跑遍历；
一开始写的跟高赞答案里一样的 DFS，面试官说可以再简化一下，然后发现可以直接比较下标范围来确定左子树还是右子树；
最后让解释了一下时间复杂度，由于已经写得昏头了这段答得磕磕巴巴，面试官疯狂提示，也算是回答出来了。

find path within Fibonacci tree
题目不提供node structure，你要自己写一个也不行

input 是 order: int，start: int， end: int。找从start 到 end 的最短路线

一上来讲了个暴力解思路，国人小哥哥让我利用这个tree的特性想个optimal solution...疑惑了半天这example 里的node value 也不等于left node + right node.....到底Fibonacci在哪里？他提醒后才发现在 tree size，和node value无关

大概就是 每个tree size是left child tree size+ right child tree size + 1

for example: size(T_5) = size(T_4) + size(T_3) + 1 （这里的3，4，5 是order）

就。。。这题为啥要叫Fibonacci tree呢？不是所有binary tree 都左边的size加右边的size 加1吗？换名！

还有一个正儿八经关键的特性是每个tree 是从0 到 n-1 （n是size of tree）pre-order label的

弄清楚这俩特性 我才讲出time space 都是O（order）的正确的解题思路 也理解了为啥不用node structure，直接处理int就行。。到这里已经花了20多分钟了

大概就是搞个O(order) size的array 储存每个 subtree的size，然后找path to start和path to end. 最后处理一下这两个path.

写code 的时候磕磕绊绊，我想recursion一般都pass in curr_node，也就这么写了，小哥一直说不用，我又试着去理解他的想法 (我理解大概就是recursive call 的时候target 减一下sub tree size) ...然后按照他的提示后就没有然后了，大脑改思路后短路，时间也不够. 没有写出working code 铁挂。结束后在stackoverflow找到了一模一样的题目，高赞答案就pass in current node。小哥之前的hint都有帮助，所以最后这个不敢忽略，感觉他也想帮我尽快写出来。。。但其实完全可以坚持自己的想法，正确答案不只有一个
"""