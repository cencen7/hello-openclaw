"""
大概就是要实现一个LazyArray类，需要支持查询特定元素的第一个index，
要求实现一个map接口，传入的是一个函数指针，这个函数会对每个元素进行操作，但是不能立即操作
，而是直到调用indexof这个函数的时候才会按顺序执行之前传入的所有函数进行更新，重点是调用map后，
需要返回一个新的对象，包括当前的对象+新传入的函数指针，而不是在原对象上in place更新。
这个地方我还特意问了面试官是要哪种，他一开始说都行，结果后来我选了一个写完他又说不行。
体验是题很简单，但是难度就是搞清楚到底是什么要求，
全程不是“what do you think this should be like“就是”up to you"，
甚至感觉有的问题问了之后干脆就得不到回答，然后回过头来又不行
（怀疑根本没pay attention），既然说不清楚那只能我在这里说清楚了。

---
很多followup，比如如何用caching减少运算，要自己写test case验证laziness
---
上来就给了API，然后让我猜Api什么样的behavior才更符合用户的期待。
注意需要test lazyness，用wrapper或者mock check function invocation times
lazy array，要求实现 array.map(...).indexOf(...)，
其中map传进去一个function，indexOf返回运行了所有function之后传入值的index。
要求map的操作最后再做，所以叫lazy array。For example:
arr = LazyArray([10, 20, 30, 40, 50])
arr.map(lambda x:x*2).indexOf(40) ----> 1
arr.map(lambda x:x2).map(lambda x:x3).indexOf(240)
 ----> 3 注意这里重新开了一个chain，上一行的map就不计算在内了
 Each map() must return a new LazyArray, because chains are independent

"""