# Binary search solution to: https://leetcode.com/problems/koko-eating-bananas/description/

class Solution:
    def time(self, piles, h, s):
        t = 0
        for i in piles:
            t += math.ceil(i / s)
            if t > h:
                return False
        return True

    def minEatingSpeed(self, piles, h):
        low, high = 1, max(piles)
        ans = high
        while low <= high:
            mid = (low + high) // 2
            if self.time(piles, h, mid):
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans