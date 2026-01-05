"""

面经原题 Find Optimal Commute，我提出了使用dijkstra算法，讲了思路和时间/空间复杂度。面试官提示说这道题可以再优化，没有必要用dijkstra。我提出了可以对每一种given mode，使用传统的BFS并计算cost/time，最后做比较，简述了时间/空间复杂度。面试官表示make sense可以开始写了。这部分沟通用了15分钟。


开始一边说一边写，bfs部分比较顺利写完了，试运行了一下有些int/str 小bug，很快改掉。

但最后比较每一个mode cost/time，因为要考虑duplicate的情况，面试官说不能sort，要O(n)，脑子短路了半天没想出来，其实很简单！！最后我说时间不太够我能先不考虑duplicate，跑一下完整代码不？老哥说可以。手写了一下test case，跑成功了。然后只剩5分钟。

面试官说只有五分钟了就问我对他有啥问题，我问了oncall累不累/今年有啥新项目，老哥说oncall之前蛮重的，新项目的话思考了好一会儿，我听下来这个组operation占大头，说了一下我之前的组oncall也很重blabla。

You have a simplified map of San Francisco. It is a 2D grid. Each square on the grid is one of these:

'S': Your Home (Start).
'D': Your Office (Destination).
A digit '1' to 'k': A street that only allows one specific type of travel (like a bike lane or bus route).
'X': A roadblock. You cannot go here.
You also get three lists (arrays) of length k:

modes: The names of the travel types (e.g., ["bike", "bus"]).
times: How many minutes it takes to move one block for each mode.
costs: How many dollars it costs to move one block for each mode.
Rules for Moving
You can move up, down, left, or right. You cannot move diagonally.
You must stay on the same travel mode (the same digit) for the whole trip.
You cannot switch modes in the middle of the trip.
You cannot step on a different number or an 'X'.
For each mode i, the time and cost to move one block are found in times[i] and costs[i].

To find the total time and total cost, you add up the time and cost for every numbered block you step on. The start ('S') and end ('D') blocks are free. They do not add to the time or cost.

Goal
Find the name of the travel mode that gets you from 'S' to 'D' in the least amount of time.

If two modes have the exact same time, pick the one that costs less money.
If there is no way to reach the office, return an empty string "".
Example Case
Input:
grid = [
    ['S', '1', '1', '1', 'D'],
    ['2', '2', '2', '2', 'X']
]

modes = ["bike", "bus"]
times = [5, 3]
costs = [2, 1]
Explanation:
The map looks like this:

Row 0: S   1   1   1   D
Row 1: 2   2   2   2   X
Mode 1 (bike): You can go from S to D.

Path: S → 1 → 1 → 1 → D
Distance: You stepped on 3 "bike" blocks.
Time: 3 blocks × 5 minutes = 15 minutes.
Cost: 3 blocks × 2 dollars = 6 dollars.
Mode 2 (bus): You cannot reach D.

Path: S → 2 → 2 → 2 → 2... but then you hit 'X'.
The bus path is blocked.
Output:
"bike"  # This is the only way to get there
Input Limits
The grid size is between 1x1 and 100x100.
There are between 1 and 4 travel modes (k).
Time and cost values are between 1 and 100.
There is exactly one 'S' and one 'D'.

optimal commute原题，follow up是转弯有cost怎么办

-----

就是上周的面试，考的是Optimal Commute 这道题
You are commuting across a simplified map of San Francisco, represented as a 2D grid. Each cell on the grid is one of the following:
'S'

: Your home location (starting point).
'D'

: Your office location (destination).
A digit from 
'1'

 to 
k

: A street segment reserved for exactly one transportation mode.
'X'

: An impassable roadblock.

You are also given three arrays with length 
k

:
modes

: The name of each available transportation mode.
times

: The time (in minutes) required to traverse a single block using each mode.
costs

: The cost (in dollars) to traverse a single block using each mode.

Movement is allowed up, down, left, and right. You may only travel along contiguous cells of the same transportation mode (i.e., same digit). You cannot move between cells of different modes, nor can you cross roadblocks.
For each mode 
i

, the time and cost to traverse a single block are given by 
times

 and 
costs

, respectively. The total travel time and cost are calculated as the sum of the time and cost for each cell visited along the path from 
'S'

 to 
'D'

.
Return the name of the transportation mode that yields the minimum total time from 
'S'

 to 
'D'

. If multiple modes result in the same minimum time, return the one with the lowest total cost. Return an empty string if no valid route exists.

我用了普通的bfs，followup 是怎么样能把 time complexity降成 rc 而不是krc，给了点提示，后续过了两个小时说过了 到hr info call
----

前几周面的Databrick 店面， 考的find optimal commute 原题。 找出从起点到终点花费时间最短的模式。 如果时间相同就花费最小的模式，例如bike， walk， car之类的。 给了一个 matrix，里面 “1”“2”“3”“4” 表不同的交通模式，还给了cost和time array for each mode.

上来提出用min-heap 来存每个cell 从起点开始的
(累计时间, 累计cost)

，扫一遍matrix 拿到最优模式。面试官不同意，觉得time complexity不好。 我在提出用 BFS for each mode, 得跑4遍 ，面试官觉得最好跑一遍 BFS就行。来回沟通半天，最后我也只会写跑4遍的BFS， 还没剩时间跑test了。
---
二维Matrix，上面都是string, 'S'代表起点，'D'代表终点，数字'1'-'N'分别是N种交通工具的编号;
一个list，代表交通工具每走一步的cost
另一个list，代表交通工具每走一步的time

要求：只准上下左右；不准换交通工具。
返回：最佳交通工具编号，即总time最短的前提下，总cost最少的。
可以每个交通工具BFS一次，求出各自的总time和总cost，最后对比一下就好了。

--
https://www.1point3acres.com/home/pins/887099
"""