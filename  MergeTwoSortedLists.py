"""
LeetCode 21. Merge Two Sorted Lists 
"""

from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val       
        self.next = next     


class Solution:

    # Approach 1: Collect Values, Sort, Rebuild
    # Idea:
    #   Dump every value from both lists into a Python list, sort it, and
    #   build a bran -new linked list from the sorted values.
    #
    # Downsides: ignores that the inputs are ALREADY sorted (so the sort is
    #   wasted work), and creates new nodes instead of reusing the given ones.
    #
    # TC: O((n+m) log(n+m))  : the sort
    # SC: O(n+m)             : the values list and the new nodes
    def mergeTwoLists_sort(self, list1: Optional[ListNode],
                           list2: Optional[ListNode]) -> Optional[ListNode]:
        vals = []
        for node in (list1, list2):
            while node:
                vals.append(node.val)
                node = node.next
        vals.sort()

        dummy = ListNode()
        tail = dummy
        for v in vals:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next


    # Approach 2: Iterative with a Dummy Node (Standard)
    # Idea:
    #   Like merging two sorted piles of cards: look at the front of each
    #   list, attach the SMALLER node to the end of the merged list, and
    #   advance in that list. When one list runs out, attach the rest of
    #   the other in one step (it's already sorted and >= everything so far).
    #
    # Dummy node: a throwaway node placed in front of the merged list, so
    #   EVERY node (including the first) is attached the same way with
    #   tail.next = ... . No special case for "is the merged list empty?".
    #   Return dummy.next, the real head.
    #
    # TC: O(n+m)  : each node attached exactly once
    # SC: O(1)    : only the dummy is created; existing nodes are relinked
    def mergeTwoLists(self, list1: Optional[ListNode],
                      list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next

        tail.next = list1 if list1 else list2
        return dummy.next


    # Approach 3: Recursive
    # Idea:
    #   The smaller of the two front nodes must come first. Its .next is
    #   "the merge of everything that's left", which is the same problem on
    #   a smaller input, so recurse.
    #   Base cases: if one list is empty, the answer is the other list.
    #
    # TC: O(n+m)  : one call per node
    # SC: O(n+m)  : call stack (one frame per node)
    def mergeTwoLists_recursive(self, list1: Optional[ListNode],
                                list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists_recursive(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists_recursive(list1, list2.next)
            return list2


def build_list(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def to_pylist(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


# Quick local test (LeetCode ignores this part)
if __name__ == "__main__":
    sol = Solution()
    tests = [
        ([1, 2, 4], [1, 3, 4], [1, 1, 2, 3, 4, 4]),
        ([], [], []),
        ([], [0], [0]),
        ([5], [1, 2, 3], [1, 2, 3, 5]),
        ([-3, 0, 7], [-5, 10], [-5, -3, 0, 7, 10]),
    ]
    for a, b, expected in tests:
        results = (
            to_pylist(sol.mergeTwoLists_sort(build_list(a), build_list(b))),
            to_pylist(sol.mergeTwoLists(build_list(a), build_list(b))),
            to_pylist(sol.mergeTwoLists_recursive(build_list(a), build_list(b))),
        )
        status = "OK" if all(r == expected for r in results) else "MISMATCH"
        print(f"{status}  {a} + {b}: {results}  expected {expected}")