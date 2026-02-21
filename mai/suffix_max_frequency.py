"""
Problem: Suffix Maximum Frequency Queries (from 1point3acres)

Given an integer array nums of length n and a query array query of length m. For each query index q = query[i], return the number of occurrences of the maximum value in the suffix subarray nums[q..n-1].

Return an array ans of length m.

Example:
    nums = [7, 5, 7, 2, 7], query = [0, 1, 2, 3, 4] -> [3, 2, 2, 1, 1].

Requirements:
- Better than scanning the suffix for each query.

Constraints:
- 1 <= n, m <= 2e5
- -1e9 <= nums[i] <= 1e9
- 0 <= query[i] < n
"""

from typing import List

def solution(nums: List[int], query: List[int]) -> List[int]:
    # use O(n) space to store max_in_ss
    # max_in_ss[i]: max val in suffix subarray nums[i...n-1]
    # for every query, we just need to look at index max_in_ss[q]
    l = len(nums)
    max_in_ss = [0] * l
    max_value = float('-inf')
    cur_max_cnt = 0
    for i in range(l-1, -1, -1):
        if nums[i] > max_value:
            max_value = nums[i]
            cur_max_cnt = 1
        elif nums[i] == max_value:
            cur_max_cnt += 1
        max_in_ss[i] = cur_max_cnt
    return [max_in_ss[q] for q in query]

if __name__ == "__main__":
    nums = [7, 5, 7, 2, 7]
    query = [0, 1, 2, 3, 4]
    res = solution(nums, query)
    print(res)
