"""
LeetCode Problem #23 — Merge k Sorted Lists (Hard)
-------------------------------------------------
You are given an array of k linked-lists, each of which is sorted in ascending order.
Merge all the linked lists into one sorted linked list and return it.

Example:
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]

"""

import heapq

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeKLists(self, lists):
        # Min-heap to store (node value, list index, node reference)
        min_heap = []

        # Initialize the heap with the first node of each list
        for i, node in enumerate(lists):
            if node:
                heapq.heappush(min_heap, (node.val, i, node))

        dummy = ListNode(0)
        current = dummy

        while min_heap:
            # Extract the smallest node
            val, i, node = heapq.heappop(min_heap)
            current.next = node
            current = current.next

            # If there are more nodes in this list, push the next node into the heap
            if node.next:
                heapq.heappush(min_heap, (node.next.val, i, node.next))

        return dummy.next


# Example test
# Helper function to build and print linked lists
def build_linked_list(values):
    dummy = ListNode(0)
    curr = dummy
    for val in values:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next

def print_linked_list(node):
    res = []
    while node:
        res.append(node.val)
        node = node.next
    return res

# Example usage
if __name__ == "__main__":
    lists = [
        build_linked_list([1,4,5]),
        build_linked_list([1,3,4]),
        build_linked_list([2,6])
    ]

    result = Solution().mergeKLists(lists)
    print("Merged Linked List:", print_linked_list(result))
