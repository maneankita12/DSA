"""
LeetCode 3. Longest Substring Without Repeating Characters  (Medium)
Problem: Given a string s, return the length of the longest substring
(continuous, no skipping) that contains no repeated characters.
"""


class Solution:

    # Approach 1: Brute Force
    # Idea:
    #   Try every starting index i. From i, extend j to the right, adding
    #   characters to a set. Stop as soon as a character repeats.
    #   Track the longest length seen (j - i + 1).
    #
    # Downside: restarts from scratch at every i, re checking characters
    #   it already looked at.
    #
    # TC: O(n^2)  : two nested loops over the string
    # SC: O(min(n, m))  : the set holds at most one copy of each character
    #                     (m = size of the character set, e.g. 128 for ASCII)
    def lengthOfLongestSubstring_bruteforce(self, s: str) -> int:
        best = 0
        for i in range(len(s)):
            seen = set()
            for j in range(i, len(s)):
                if s[j] in seen:
                    break
                seen.add(s[j])
                best = max(best, j - i + 1)
        return best

    # Approach 2: Sliding Window with a Set
    # Idea:
    #   Keep a window [left, right] that never contains a repeat.
    #   : Move right forward one character at a time.
    #   : If s[right] is already in the window, move left forward
    #     (removing s[left] from the set) until the duplicate is gone.
    #   : Add s[right], then update best with the window size.
    #
    # each character is added once and removed at most once,
    #   so nothing is re checked from scratch.
    #
    # TC: O(n)  : at most 2n set operations (each char enters/leaves once)
    # SC: O(min(n, m))  : the set holds the current window's characters
    def lengthOfLongestSubstring_set(self, s: str) -> int:
        seen = set()
        left = 0
        best = 0
        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            best = max(best, right - left + 1)
        return best

    # Approach 3: Sliding Window with Last-Seen Index (Optimal)
    # Idea:
    #   Store the last index where each character appeared.
    #   When s[right] was seen before AND that index is inside the current
    #   window (last_seen[c] >= left), jump `left` straight to
    #   last_seen[c] + 1 instead of creeping forward one step at a time.
    #
    # Why the `>= left` check: an old copy to the left of the window was
    #   already dropped, so it isn't a real duplicate. Without this check,
    #   `left` could move backward (e.g. "abba").
    #
    # TC: O(n)  : single pass, each step is O(1)
    # SC: O(min(n, m))  : dict stores one index per distinct character
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        left = 0
        best = 0
        for right, c in enumerate(s):
            if c in last_seen and last_seen[c] >= left:
                left = last_seen[c] + 1
            last_seen[c] = right
            best = max(best, right - left + 1)
        return best


if __name__ == "__main__":
    sol = Solution()
    tests = [("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("", 0), ("abba", 2)]
    for s, expected in tests:
        results = (
            sol.lengthOfLongestSubstring_bruteforce(s),
            sol.lengthOfLongestSubstring_set(s),
            sol.lengthOfLongestSubstring(s),
        )
        print(f"{s!r}: {results}  expected {expected}")