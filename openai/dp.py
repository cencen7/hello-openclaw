"""
the Edge of [a, b] can not be put into the same group where a, b is in zip(allergic, poisonous).
 The question is what is the number of continuous range that we can have to make sure all elements in this range are valid. 
 The range can not be empty, 
 however, only one element is allowed.
For example, if we have n = 5
allergic is [1,2]
poisonous is [3, 5]
The valid ranges will be
[1]
[1,2], [2]
[2,3],[3]
[2,3,4],[3,4],[4]
[3,4,5],[4,5],[5]

A quick idea about how to solve it
After reading this example, we will be clear that the left-most bolded number is critical to the final answer. If we have that number, we can use the following simple way to solve the problem.
for i in range(1, n+1):
    res += i - left_most_number in this row +1
How to find the leftmost number?
Firstly, we collect all the information given the node i, what is the largest number of a node on its left side that it can not stay together with.
In the example, we will have the results below after we process all the information provided in allergic, poisonous. -1 means no node will confilct with this node.
i= 1, largest number of a node on its left side it can not stay with = -1
i = 2, largest number of a node on its left side it can not stay with = -1
i = 3, largest number of a node on its left side it can not stay with= 1
i = 4,largest number of a node on its left side it can not stay with= -1
i = 5, largest number of a node on its left side it can not stay with= 2

"""

import collections
def bio_hazard(n, allergic, poisonous):
    # find the conflicting pair such as (1,3) and (2,5)
    # for 3, most left is 1
    # for 5, most left is 2
    d = collections.defaultdict(lambda :-1)
    for a, b in zip(allergic, poisonous):
        a, b = sorted([a, b])
        d[b] = max(d[b], a)
        
    # this is to fix when 4,, left most should be 2, not -1
    for i in range(1, n + 1):
        d[i] = max(d[i], d[i - 1])
    
    # count the `left most` number in the range by using i - left_most_number + 1
    res = 0
    for i in range(1, n+1):
        if d[i]==-1:
            res += i
        else:
            res += i-d[i]
    return res

# Example usage:
n = 5
allergic = [1, 3]
poisonous = [2, 5]
print(bio_hazard(n, allergic, poisonous))
