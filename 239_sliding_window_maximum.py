"""
LeetCode Problem #239 — Sliding Window Maximum (Hard)
-----------------------------------------------------
You are given an array nums and an integer k.
Return the maximum value in each sliding window of size k.

Example:
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]

"""

from collections import deque

class Solution:
    def maxSlidingWindow(self, nums, k):
        n = len(nums)
        if not nums or k == 0:
            return []

        dq = deque()  # stores indices
        result = []

        for i in range(n):
            # Remove elements outside the window (left side)
            while dq and dq[0] < i - k + 1:
                dq.popleft()

            # Remove all elements smaller than current (not useful)
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()

            # Add current element's index
            dq.append(i)

            # Append current window's max to result
            if i >= k - 1:
                result.append(nums[dq[0]])

        return result


# Example usage
if __name__ == "__main__":
    nums = [1,3,-1,-3,5,3,6,7]
    k = 3
    print("Sliding Window Maximum:", Solution().maxSlidingWindow(nums, k))
