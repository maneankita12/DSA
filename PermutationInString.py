"""
Permutation in String 

Problem: Given strings s1 and s2, return True if s2 contains a permutation
of s1, i.e. some substring of s2 uses exactly the same letters as s1 in
any order.

Notation: n = len(s2), m = len(s1);
"""

from collections import Counter


class Solution:

    # Approach 1: Brute Force (recount every window)
    # Idea:
    #   For every start i, slice the window s2[i:i+m], count its letters
    #   with Counter, and compare with Counter(s1). Equal counts (order
    #   doesn't matter) means the window is a permutation of s1.
    #
    # range(len(s2) - m + 1) = number of starts that leave room for a full
    #   window. If m > len(s2) the range is empty, so we return False.
    #
    # Downside: each window is copied and counted from scratch, even though
    #   neighboring windows share all but one letter.
    #
    # TC: O(n * m)  :  approx n windows, each sliced and counted in O(m)
    # SC: O(m)      : the slice and its Counter
    def checkInclusion_bruteforce(self, s1: str, s2: str) -> bool:
        m = len(s1)
        need = Counter(s1)
        for i in range(len(s2) - m + 1):
            if Counter(s2[i:i + m]) == need:
                return True
        return False

    # Approach 2: Sliding Window + compare 26 slot arrays
    # Idea:
    #   Keep two 26 slot tally arrays (slot = ord(c) - ord('a')):
    #     need   = counts for s1
    #     window = counts for the current window of s2
    #   For each i:
    #   : ADD s2[i] (the new letter on the right).
    #   : Once i >= m, REMOVE s2[i - m] (the letter that slid out on the
    #     left; the window should cover indices i-m+1 .. i).
    #   : If window == need (26 slot by slot comparisons), return True.
    #
    # TC: O(26 * n) = O(n)  : O(1) add/remove + 26 slot compare per step
    # SC: O(1)              : two fixed 26 slot arrays
    def checkInclusion_window(self, s1: str, s2: str) -> bool:
        m = len(s1)
        if m > len(s2):
            return False

        need = [0] * 26
        window = [0] * 26
        for c in s1:
            need[ord(c) - ord('a')] += 1

        for i in range(len(s2)):
            window[ord(s2[i]) - ord('a')] += 1
            if i >= m:
                window[ord(s2[i - m]) - ord('a')] -= 1
            if window == need:
                return True
        return False

    # Approach 3: Sliding Window + matches counter (Optimal)
    # Idea:
    #   Instead of comparing all 26 slots every step, keep
    #     matches = how many of the 26 slots have window[i] == need[i]
    #   matches == 26 -> every count agrees -> permutation found.
    #   (Letters in neither string count as matches: 0 == 0. That's why the
    #   target is 26, not len(s1).) Same idea as have/required in LC 76.
    #
    #   Setup: fill need with s1 and window with the first m letters of s2,
    #   then count the starting matches.
    #
    #   Each slide changes only 2 slots, so only they can change matches:
    #   : ADD (count went up by 1):
    #       now == need      : was too few, just started matching, +1
    #       now == need + 1  : was exact, just stopped matching, -1
    #   : REMOVE (count went down by 1):
    #       now == need      : was too many, just started matching, +1
    #       now == need - 1  : was exact, just stopped matching, -1
    #   Any other case: slot was wrong before and is still wrong.
    #
    #   The matches == 26 check runs BEFORE each slide, so the final
    #   `return matches == 26` checks the last window.
    #
    # TC: O(n + m)  : setup O(m + 26), then O(1) per slide
    # SC: O(1)      : two fixed 26 slot arrays
    def checkInclusion(self, s1: str, s2: str) -> bool:
        m = len(s1)
        if m > len(s2):
            return False

        need = [0] * 26
        window = [0] * 26
        for i in range(m):
            need[ord(s1[i]) - ord('a')] += 1
            window[ord(s2[i]) - ord('a')] += 1

        matches = sum(1 for i in range(26) if need[i] == window[i])

        for right in range(m, len(s2)):
            if matches == 26:
                return True

            idx = ord(s2[right]) - ord('a')
            window[idx] += 1
            if window[idx] == need[idx]:
                matches += 1
            elif window[idx] == need[idx] + 1:
                matches -= 1

            idx = ord(s2[right - m]) - ord('a')
            window[idx] -= 1
            if window[idx] == need[idx]:
                matches += 1
            elif window[idx] == need[idx] - 1:
                matches -= 1

        return matches == 26


# Quick local test 
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("ab", "eidbaooo", True),
        ("ab", "eidboaoo", False),
        ("abc", "ab", False),       
        ("ab", "ab", True),         
        ("ab", "xxba", True),       
        ("aab", "abbb", False),     
        ("adc", "dcda", True),
    ]
    for s1, s2, expected in tests:
        results = (
            sol.checkInclusion_bruteforce(s1, s2),
            sol.checkInclusion_window(s1, s2),
            sol.checkInclusion(s1, s2),
        )
        status = "OK" if all(r == expected for r in results) else "MISMATCH"
        print(f"{status}  s1={s1!r}, s2={s2!r}: {results}  expected {expected}")