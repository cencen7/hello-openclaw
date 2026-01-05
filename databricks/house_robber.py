"""
最近Phone Screen就是House Robber I, 需要optimize space 才能过

https://leetcode.com/problems/house-robber/
https://leetcode.com/problems/house-robber-ii/
"""
from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        money[i]: max amount of money we can rob at the state of house i
        money[i] = max(money[i-1], money[i-2] + nums[i])


        money[0] = nums[0]
        money[1] = max(nums[0], nums[1])
        money[2] = max(money[0] + nums[2], money[1])
        """
        if len(nums) == 0:
            return 0
        if len(nums) == 1:
            return nums[0]
        
        # do initialization
        money = [0 for _ in range(len(nums))]

        # initial condition
        money[0] = nums[0]
        money[1] = max(nums[0], nums[1])

        for i in range(2, len(nums)):
            money[i] = max(money[i-1], money[i-2] + nums[i])
        
        return money[-1]
    

class SolutionCircle:
    def rob(self, nums: List[int]) -> int:
        """
        money[i]: max amount of money we can rob at the state of house i

        two arrays to track cirle status:
        rob first:
            money_rob_first[1] = nums[0]
            money_rob_first[i] = money_rob_first(money[i-1], money[i-2] + nums[i])
            return with money[-2]
        not rob first
            money_not_rob_first[1] = nums[1]
            money_not_rob_first[i] = money_not_rob_first(money[i-1], money[i-2] + nums[i])
            return with money[-1]

        compare two and finally return the last one
        """
        if len(nums) == 0:
            return 0
        if len(nums) == 1:
            return nums[0]
        
        # do initialization
        money_rob_first = [0 for _ in range(len(nums))]
        money_not_rob_first = [0 for _ in range(len(nums))]

        # initial condition
        money_rob_first[0] = nums[0]
        money_rob_first[1] = nums[0]
        
        money_not_rob_first[0] = 0
        money_not_rob_first[1] = nums[1]

        for i in range(2, len(nums)):
            money_rob_first[i] = max(money_rob_first[i-1], money_rob_first[i-2] + nums[i])
            money_not_rob_first[i] = max(money_not_rob_first[i-1], money_not_rob_first[i-2] + nums[i])
        
        return max(money_rob_first[-2], money_not_rob_first[-1])
    

class SolutionCircle2(object):
    def _rob(self, nums, start, end):
        rob, not_rob = 0, 0
        for idx in range(start, end):
            num = nums[idx]
            rob, not_rob = not_rob + num, max(rob, not_rob)
        return max(rob, not_rob)
                
    def rob(self, nums):
        """
        dp[i][s]: max amount of money can rob with status 0: not robbed this time, 1: robbed this time
        dp[i][1] = dp[i-1][0] + nums[i]
        dp[i][0] = max(dp[i-1][1], dp[i-1][0])
        """
        if not nums:
            return 0
        n = len(nums)
        
        if len(nums) == 1:
            return nums[0]
        
        return max(self._rob(nums, 1, n), self._rob(nums, 0, n - 1))

