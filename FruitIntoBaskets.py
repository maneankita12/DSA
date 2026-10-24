"""
LeetCode 904. Fruit Into Baskets 

Problem: fruits[i] is the type of fruit on tree i. You have 2 baskets,
each holding ONE type (any amount). Start at any tree and pick one fruit
from every tree moving right, no skipping; stop when a fruit fits in
neither basket. Return the max number of fruits you can pick.

Translated: length of the longest continuous subarray with
AT MOST 2 DISTINCT values.
"""


class Solution:


    # 1: Brute Force
    # Idea:
    #   For each start i, walk j to the right, adding fruit types to a
    #   set. The moment a 3rd type appears, `break`. Otherwise record the
    #   length j - i + 1.
    #
    # Why break is safe: once a window from i has 3 types, every longer
    #   window from i has at least 3 types too.
    #
    # TC: O(n^2)  : each start can scan to the end
    # SC: O(1)    : the set never holds more than 3 types
    def totalFruit_bruteforce(self, fruits: list[int]) -> int:
        best = 0
        for i in range(len(fruits)):
            types = set()
            for j in range(i, len(fruits)):
                types.add(fruits[j])
                if len(types) > 2:
                    break
                best = max(best, j - i + 1)
        return best

    # 2: Sliding Window + count dict 
    # Idea:
    #   basket = {fruit type: how many in the window}
    #   : GROW: move right, add fruits[right] to basket.
    #   : SHRINK: while len(basket) > 2 (3 types), drop fruits[left],
    #     move left forward.
    #   : RECORD: window is valid, update best.
    #
    # Key detail: `del basket[f]` when a count hits 0. len(basket) means
    #   "number of types in the window", so a leftover f:0 key would make
    #   a valid window look invalid.
    #
    # TC: O(n)  : each fruit enters once and leaves at most once
    # SC: O(1)  : basket holds at most 3 keys
    def totalFruit(self, fruits: list[int]) -> int:
        basket = {}
        left = 0
        best = 0
        for right in range(len(fruits)):
            basket[fruits[right]] = basket.get(fruits[right], 0) + 1

            while len(basket) > 2:
                f = fruits[left]
                basket[f] -= 1
                if basket[f] == 0:
                    del basket[f]
                left += 1

            best = max(best, right - left + 1)
        return best


if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 2, 1], 3),
        ([0, 1, 2, 2], 3),
        ([1, 2, 3, 2, 2], 4),
        ([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4], 5),
        ([0], 1),
        ([1, 1, 1, 1], 4),
        ([1, 0, 1, 4, 1, 4, 1, 2, 3], 5),
    ]
    for fruits, expected in tests:
        results = (
            sol.totalFruit_bruteforce(fruits),
            sol.totalFruit(fruits),
        )
        status = "OK" if all(r == expected for r in results) else "MISMATCH"
        print(f"{status}  fruits={fruits}: {results}  expected {expected}")