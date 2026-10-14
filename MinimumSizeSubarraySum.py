"""
LeetCode 209. Minimum Size Subarray Sum

Given an array of POSITIVE integers nums and a target, return the
length of the shortest continuous subarray whose sum is >= target.
If there is no such subarray, return 0.

"""

from bisect import bisect_left


class Solution:

    # Approach 1: Brute Force
    # Idea:
    #   For each start i, reset total to 0 and keep adding nums[j] until
    #   total >= target. Record the length j - i + 1, then `break`:
    #   adding more numbers only makes the subarray longer.
    #
    # TC: O(n^2)  : each of the n starts can scan to the end
    # SC: O(1)    : only total, best, i, j
    def minSubArrayLen_bruteforce(self, target: int, nums: list[int]) -> int:
        best = float("inf")
        for i in range(len(nums)):
            total = 0
            for j in range(i, len(nums)):
                total += nums[j]
                if total >= target:
                    best = min(best, j - i + 1)
                    break
        return 0 if best == float("inf") else best

    # Approach 2: Sliding Window (Optimal)
    # Idea:
    #   Keep a window [left, right] and its running sum `total`.
    #   : GROW: move right, add nums[right] to total.
    #   : SHRINK: while total >= target (window is valid), record its
    #     length, subtract nums[left], and move left forward.
    #   When total drops below target, go back to growing.
    #
    # Why it needs POSITIVE numbers: adding always increases the sum and
    #   removing always decreases it. With negatives, removing a number
    #   could increase the sum, and the grow/shrink logic breaks.
    #
    # TC: O(n)   right moves n times; left moves at most n times in
    #             total because it never goes back
    # SC: O(1)   only left, total, best
    def minSubArrayLen(self, target: int, nums: list[int]) -> int:
        left = 0
        total = 0
        best = float("inf")

        for right in range(len(nums)):
            total += nums[right]

            while total >= target:
                best = min(best, right - left + 1)
                total -= nums[left]
                left += 1

        return 0 if best == float("inf") else best

    # Approach 3: Prefix Sum and Binary Search (LeetCode follow up)
    # Idea:
    #   prefix[k] = sum of the first k numbers (prefix[0] = 0), so
    #   sum(nums[i..j-1]) = prefix[j] - prefix[i].
    #   For each start i, find the smallest j with
    #   prefix[j] >= prefix[i] + target. Length = j - i.
    #
    # Why binary search works: all numbers are positive, so prefix only
    #   increases, i.e. it's sorted. bisect_left finds the first index
    #   whose value is >= what we ask for, in O(log n).
    #
    # Slower than the sliding window, but it's what the follow-up asks
    #   for, and a good intro to prefix sums and binary search.
    #
    # TC: O(n log n)  : n binary searches, each O(log n)
    # SC: O(n)        : the prefix list
    def minSubArrayLen_binary(self, target: int, nums: list[int]) -> int:
        prefix = [0]
        for num in nums:
            prefix.append(prefix[-1] + num)

        best = float("inf")
        for i in range(len(nums)):
            j = bisect_left(prefix, prefix[i] + target)
            if j < len(prefix):
                best = min(best, j - i)
        return 0 if best == float("inf") else best

if __name__ == "__main__":
    sol = Solution()
    tests = [
        (7, [2, 3, 1, 2, 4, 3], 2),
        (4, [1, 4, 4], 1),
        (11, [1, 1, 1, 1, 1, 1, 1, 1], 0),
        (11, [1, 2, 3, 4, 5], 3),
        (15, [1, 2, 3, 4, 5], 5),
        (3, [5], 1),
    ]
    for target, nums, expected in tests:
        results = (
            sol.minSubArrayLen_bruteforce(target, nums),
            sol.minSubArrayLen(target, nums),
            sol.minSubArrayLen_binary(target, nums),
        )
        status = "OK" if all(r == expected for r in results) else "MISMATCH"
        print(f"{status}  target={target}, nums={nums}: {results}  expected {expected}")