"""
76. Minimum Window Substring 
Problem: Given strings s and t, return the shortest substring of s that
contains every character of t, including duplicates. If no such
substring exists, return "".


Notation for complexity:
    n = len(s), m = len(t)
    k = number of distinct characters in t
    Σ = size of the character set (52 for upper + lowercase English)
"""

from collections import Counter


class Solution:

    # Approach 1: True Brute Force (generate every substring)
    # Idea:
    #   Generate every substring s[i..j], count its letters from scratch
    #   with Counter, and check if it has at least as many of each letter
    #   as t needs. Keep the shortest valid one.
    #
    # TC: O(n^3)  : n^2 substrings, each copied and counted in O(n)
    # SC: O(n + Σ) : the substring copy plus its Counter
    def minWindow_naive(self, s: str, t: str) -> str:
        if not s or not t or len(s) < len(t):
            return ""

        t_count = Counter(t)
        min_len = float("inf")
        ans = ""

        for i in range(len(s)):
            for j in range(i, len(s)):
                sub = s[i:j + 1]
                sub_count = Counter(sub)

                possible = True
                for char in t_count:
                    if sub_count[char] < t_count[char]:
                        possible = False
                        break

                if possible and len(sub) < min_len:
                    min_len = len(sub)
                    ans = sub

        return ans


    # Approach 2: Smarter Brute Force (incremental count + early break)
    # Idea:
    #   For each start i, extend j to the right, adding one letter at a
    #   time to a running Counter (no recounting). As soon as the window
    #   covers t, save it if it's the shortest so far, then `break`:
    #   extending further only makes it longer.
    #
    # TC: O(n^2 * k)  : approx n^2/2 extensions, each with an O(k) all() check
    # SC: O(k + Σ)    : need holds k letters, window at most Σ letters
    def minWindow_bruteforce(self, s: str, t: str) -> str:
        need = Counter(t)
        best = ""
        for i in range(len(s)):
            window = Counter()
            for j in range(i, len(s)):
                window[s[j]] += 1
                if all(window[c] >= need[c] for c in need):
                    if best == "" or j - i + 1 < len(best):
                        best = s[i:j + 1]
                    break
        return best

    # Approach 3: Sliding Window with have/required (Optimal)
    # Idea:
    #   Keep a window [left, right] and two numbers:
    #     required = how many distinct letters of t must be satisfied
    #     have     = how many are satisfied right now
    #   : GROW: move right, add s[right]. If its count just REACHED what
    #     t needs (== need[c]), have += 1. (== not >=, so extra copies
    #     don't tick the same letter twice.)
    #   : SHRINK: while have == required (window is valid), record its
    #     size if smallest, then remove s[left]. If that letter's count
    #     drops BELOW what's needed, have -= 1. Move left forward.
    #
    # TC: O(n + m)  : building need is O(m); left and right each move
    #                 at most n times in total (left never resets), and
    #                 every step is O(1) thanks to have == required
    # SC: O(k + Σ)  : need holds k letters, window at most Σ letters
    def minWindow(self, s: str, t: str) -> str:
        need = Counter(t)
        window = {}
        have, required = 0, len(need)
        best_len, best_start = float("inf"), 0
        left = 0

        for right, c in enumerate(s):
            window[c] = window.get(c, 0) + 1
            if c in need and window[c] == need[c]:
                have += 1

            while have == required:
                if right - left + 1 < best_len:
                    best_len = right - left + 1
                    best_start = left
                lc = s[left]
                window[lc] -= 1
                if lc in need and window[lc] < need[lc]:
                    have -= 1
                left += 1

        return "" if best_len == float("inf") else s[best_start:best_start + best_len]


# Quick local test
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("ADOBECODEBANC", "ABC", "BANC"),
        ("ADBANC", "ABC", "BANC"),
        ("a", "a", "a"),
        ("a", "aa", ""),
        ("aa", "aa", "aa"),
        ("ab", "b", "b"),
    ]
    for s, t, expected in tests:
        results = (
            sol.minWindow_naive(s, t),
            sol.minWindow_bruteforce(s, t),
            sol.minWindow(s, t),
        )
        status = "OK" if all(r == expected for r in results) else "MISMATCH"
        print(f"{status}  s={s!r}, t={t!r}: {results}  expected {expected!r}")
