"""
LeetCode 206. Reverse Linked List  (Easy)

Problem: Given the head of a singly linked list, reverse the list and
return the new head.
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val      
        self.next = next     


class Solution:

    # Approach 1: Copy Values, Overwrite in Reverse
    # Idea:
    #   Pass 1: walk the list, saving every value: [1, 2, 3, 4, 5].
    #   Pass 2: walk again, writing values back from the END of the list
    #   with vals.pop() (pop() removes and returns the last item).
    # Downside: swaps VALUES, not LINKS, and uses an extra list.
    #   Interviewers usually want the arrows reversed (Approach 2).
    #
    # TC: O(n)  : two passes
    # SC: O(n)  : the vals list
    def reverseList_values(self, head: Optional[ListNode]) -> Optional[ListNode]:
        vals = []
        node = head
        while node:
            vals.append(node.val)
            node = node.next

        node = head
        while node:
            node.val = vals.pop()
            node = node.next
        return head


    # Approach 2: Iterative, Three Pointers (Standard)
    # Idea:
    #   Walk the list and flip each arrow backward, one node at a time.
    #     prev = the already reversed part (starts as None: the old first
    #            node becomes the new last node, which points to None)
    #     curr = the node being flipped right now
    #     nxt  = bookmark for the rest of the list
    #   Order: SAVE, FLIP, MOVE, MOVE.
    #     nxt = curr.next     save the rest (flipping would lose it)
    #     curr.next = prev    flip this node's arrow
    #     prev = curr         move prev forward
    #     curr = nxt          move curr forward
    #   When curr is None, prev is the new head.
    #
    # TC: O(n)  : each node visited once
    # SC: O(1)  : three pointers
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    # Approach 3: Recursive
    # Idea:
    #   "Reverse everything after me, then attach myself to the end."
    #   Base case: empty list or last node -> it's the new head.
    #   After reversing head.next onward, head.next (the node right after
    #   head) is now the LAST node of the reversed part, so:
    #     head.next.next = head    that node points back to head
    #     head.next = None         head becomes the new tail
    #   new_head (the old last node) is passed back up unchanged.
    #
    # TC: O(n)  : one call per node
    # SC: O(n)  : call stack; very long lists can hit RecursionError,
    #             so the iterative version is safer
    def reverseList_recursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        new_head = self.reverseList_recursive(head.next)
        head.next.next = head
        head.next = None
        return new_head


def build_list(values):
    """[1, 2, 3] -> 1 -> 2 -> 3 -> None, returns the head."""
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_pylist(head):
    """1 -> 2 -> 3 -> None -> [1, 2, 3]"""
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# Quick local test (LeetCode ignores this part)
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]),
        ([1, 2], [2, 1]),
        ([7], [7]),
        ([], []),
    ]
    for values, expected in tests:
        results = (
            to_pylist(sol.reverseList_values(build_list(values))),
            to_pylist(sol.reverseList(build_list(values))),
            to_pylist(sol.reverseList_recursive(build_list(values))),
        )
        status = "OK" if all(r == expected for r in results) else "MISMATCH"
        print(f"{status}  {values}: {results}  expected {expected}")