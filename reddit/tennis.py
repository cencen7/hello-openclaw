"""
第一问：设计一个游戏，设计三个方法，加比分，查比分，查结果。只有2个player。
第二问写了个match的class然后在里面build game object。
需要自己写和跑test case，要求需要能够跑通。感觉考察的是OOD能力。

设计一个游戏，设计三个方法，加比分，查比分，查结果。
同时，还有几个别的要求：

必须领先两分才算胜利。如果比分超过三比三，要重置为三比三（比如四比四，五比五就要重置）
第二问转化成human score， love, deuce， 参考网球比分规则

整体来说不难，地里的经典题目，网球比分。
第一问，按照要求来就行，输出两人分数，谁是winner。
第二问， 把分数变成human score，比如30-30， 就是“deuce”。


两个人玩一个游戏，A 赢 则 A 积一分，完成以下函数：
1 输出两个人当前比分
2 积分函数，A 赢则积1分，B赢则B积分， 如果超过3比3 并且比分相同则重置比分为3：3. 如果已有获胜者 继续调这个函数则返回error。
3 winner 函数， 如果A 超过5分并且领先 B 2分 则A获胜输出A。 如果比赛没有获胜者，这个函数要返回 error
I wrote a Game class with all the methods, increment, current_score
Part2:
还是这个游戏 但是要玩5局。 谁先赢3局算赢。 更新并扩展你的函数。
GameSet
只有一个play函数，所有的logic都在这个函数里面，有一个循环，结束条件时5局或者有一个赢了三局。
在这个loop里面，创建一个game对象，然后调用increment多次，直到游戏结束。

电面，网球比赛那道题，两问。第一问写了个game的class，第二问写了个match的class然后在里面build game object
"""