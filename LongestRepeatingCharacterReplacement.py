"""
Longest Repeating Character Replacement  (Medium)
Given a string s of uppercase letters and an integer k, you may
replace at most k characters with any other letter. Return the length of
the longest substring that can be made into one repeated letter.

Notation: n = len(s); at most 26 distinct letters (uppercase English)
"""


class Solution:

    # 1: Brute Force
    # Idea:
    #   For each start i, reset count and max_freq, then extend j to the
    #   right. After adding s[j], update max_freq using just that letter.
    #   If (length - max_freq) <= k, the window is valid: record length.
    #   Otherwise `break` and try the next start.
    #
    # each new letter adds 1 to the length but at most
    # 1 to max_freq, so replacements needed never go DOWN as the window
    # grows. Once invalid from i, every longer window is invalid too.
    #
    # Downside: every new start rebuilds count from scratch.
    #
    # TC: O(n^2)  : n starts, each can scan up to n letters, O(1) per step
    # SC: O(1)    : count holds at most 26 letters
    def characterReplacement_bruteforce(self, s: str, k: int) -> int:
        best = 0
        for i in range(len(s)):
            count = {}
            max_freq = 0
            for j in range(i, len(s)):
                count[s[j]] = count.get(s[j], 0) + 1
                max_freq = max(max_freq, count[s[j]])
                if (j - i + 1) - max_freq <= k:
                    best = max(best, j - i + 1)
                else:
                    break
        return best

    # 2: Sliding Window
    # Idea:
    #   Keep one window [left, right] and one count dict.
    #    GROW: move right, add s[right] to count.
    #    SHRINK: while (length - max(count.values())) > k, the window
    #     needs too many replacements, so drop s[left] and move left.
    #    RECORD: the window is now valid, update best with its length.
    #
    # TC: O(26 * n) = O(n)  : each letter enters/leaves once, and each
    #                         check scans at most 26 counts
    # SC: O(1)              : at most 26 keys in count
    def characterReplacement_window(self, s: str, k: int) -> int:
        count = {}
        left = 0
        best = 0
        for right in range(len(s)):
            count[s[right]] = count.get(s[right], 0) + 1

            while (right - left + 1) - max(count.values()) > k:
                count[s[left]] -= 1
                left += 1

            best = max(best, right - left + 1)
        return best

    # 3: Sliding Window, never decreasing max_freq (Optimal)
    # Idea:
    #   Same as Approach 2 with two changes:
    #   1. max_freq is updated only from the letter just added, and is
    #      NEVER lowered when a letter leaves (it may become stale/too high).
    #   2. `if` instead of `while`: drop at most ONE letter per step, so
    #      the window never shrinks, it only grows or slides.
    #
    # Why a stale max_freq is safe:
    #   best can only increase if the window grows without dropping, which
    #   needs max_freq to rise. max_freq only rises when a letter REALLY
    #   reaches a new highest count in the current window. So every time
    #   best goes up, a real valid window backs it. A too-high max_freq
    #   just makes the window slide at its current size, it can never
    #   produce an answer that's too big.
    #
    # TC: O(n)  : every step is O(1), no max(count.values()) scan
    # SC: O(1)  : at most 26 keys in count
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        left = 0
        max_freq = 0
        best = 0
        for right in range(len(s)):
            count[s[right]] = count.get(s[right], 0) + 1
            max_freq = max(max_freq, count[s[right]])

            if (right - left + 1) - max_freq > k:
                count[s[left]] -= 1
                left += 1

            best = max(best, right - left + 1)
        return best


# Quick local test
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ("ABAB", 2, 4),
        ("AABABBA", 1, 4),
        ("AAAA", 0, 4),
        ("ABCD", 0, 1),
        ("ABBB", 2, 4),
        ("A", 1, 1),
        ("ABAA", 0, 2),
    ]
    for s, k, expected in tests:
        results = (
            sol.characterReplacement_bruteforce(s, k),
            sol.characterReplacement_window(s, k),
            sol.characterReplacement(s, k),
        )
        status = "OK" if all(r == expected for r in results) else "MISMATCH"
        print(f"{status}  s={s!r}, k={k}: {results}  expected {expected}")