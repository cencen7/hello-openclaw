"""
RLE BP

同时实现 encoder + decoder，面试官说重点是 encoder，decoder 算 optional
给了框架，只需要写逻辑，感觉这轮相比 DSA 就更侧重 OOP (?)
encoder
receives one int input each time (from a list), output a list of RLE/BP encoding
要求有一点点复杂，两种编码有最短长度，然后要根据输入自己判断使用哪种编码

decoder
initialized with the output of an encoder
iterator 写法

写测试
跑了几个自己写的之后，面试官又提供了一些现成的（neg values, int_max, int_min, ...）

一开始写 decoder 没认真听题，直接写的一次性输出结果，写到一半发现是个 iterator 然后尴尬地开始重写；最后测试 decoder 还是有个 bug 但是时间有点来不及了，面试官说 it's okay。

面试官给了RLE 和 Bit-Packing两种压缩方式，然后让你写一个压缩函数和对应的解压函数。压缩逻辑有点绕，需要自己判断什么时候用 RLE，什么时候用 Bit-Packing，而且还有一些约束条件，比如 RLE 至少压 8 个重复值，BP 必须正好压 8 个值。值的顺序不能打乱，也不能跳过。encode 的部分尤其复杂，decode 相对简单一些。之前好像在哪个帖看到过

-----
但不是很常见，实现一个压缩一堆正整数的encoder，把 32 位整数序列压缩成一组“run”，每个 run 使用两种编码方案之一，可以交错使用，类似[RLE, BP, RLE...]。给的输入的原始顺序不可改变。而且必须流式处理，也就是不能储存原输入。RLE：把连续相同的值编码为
(value, count)

。要求必须大于等于8个值一组。（但是最后的几个数可以少于8个数）BP：把恰好 8 个值打包为一段，值可以不同。BP 适用于没有满足 RLE 最小计数要求的地方。（也是最后几个数可以少于8个数），难点在于流式处理，然后最后几个数怎么处理（你不知道接下来会有多少数，所以任何目前最新的输入都是最后的数）。给一大堆struct和class，严格用给的类来实现。时间很紧。。一开始面试官还非要聊天，然后讲题目讲了二十分钟。。最后卡点写完，只测了最基本的没啥问题，但可能有edge case的bug，不知道是不是挂在这轮了，有点无语
----

encoder/decoder，题目是有两种已经给的encodin方式 - running length和bit packing。规则是优先使用running length，但running length至少要能encode个8个elements， 否则用bit packing
"""