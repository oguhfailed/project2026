"""
Hard Python Interview Problems — Top Tech Companies (FAANG / Big 4)
====================================================================
Topics covered:
  1.  Median of Two Sorted Arrays         — Binary Search / Divide & Conquer  O(log(m+n))
  2.  Serialize & Deserialize Binary Tree — Tree / BFS
  3.  LRU Cache                           — Doubly Linked List + Hash Map       O(1) ops
  4.  Word Ladder II                      — BFS + Backtracking
  5.  Trapping Rain Water                 — Two Pointers                        O(n)
  6.  Longest Valid Parentheses           — Stack / DP                          O(n)
  7.  Edit Distance                       — Dynamic Programming                 O(m*n)
  8.  Alien Dictionary                    — Topological Sort (Kahn's BFS)
  9.  N-Queens                            — Backtracking
  10. Sliding Window Maximum              — Monotonic Deque                     O(n)
"""

from __future__ import annotations
import heapq
from collections import defaultdict, deque
from typing import Optional


# ──────────────────────────────────────────────────────────────────────────────
# 1. Median of Two Sorted Arrays
#    Given two sorted arrays nums1 and nums2, return the median in O(log(m+n)).
#    Classic hard binary-search problem; asked at Google, Facebook, Amazon.
# ──────────────────────────────────────────────────────────────────────────────
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    """
    Binary-search on the smaller array to find the correct partition.

    Key insight: a valid partition satisfies
        max(left_half) <= min(right_half)
    for both arrays simultaneously.
    """
    # Always binary-search on the smaller array for O(log min(m,n))
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n) // 2
    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2   # partition index in nums1
        j = half - i          # partition index in nums2

        left1  = nums1[i - 1] if i > 0 else float("-inf")
        right1 = nums1[i]     if i < m else float("inf")
        left2  = nums2[j - 1] if j > 0 else float("-inf")
        right2 = nums2[j]     if j < n else float("inf")

        if left1 <= right2 and left2 <= right1:
            # Correct partition found
            if (m + n) % 2 == 1:
                return float(min(right1, right2))
            return (max(left1, left2) + min(right1, right2)) / 2.0
        elif left1 > right2:
            hi = i - 1
        else:
            lo = i + 1

    raise ValueError("Input arrays are not sorted")


# ──────────────────────────────────────────────────────────────────────────────
# 2. Serialize & Deserialize Binary Tree
#    LeetCode 297 — asked at Facebook, Amazon, Google.
#    Encode a tree to a string and decode it back to the original structure.
# ──────────────────────────────────────────────────────────────────────────────
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional["TreeNode"] = None,
                 right: Optional["TreeNode"] = None):
        self.val   = val
        self.left  = left
        self.right = right


class Codec:
    """BFS-based serialization (level-order), mirroring LeetCode's own format."""

    NULL = "null"
    SEP  = ","

    def serialize(self, root: Optional[TreeNode]) -> str:
        if not root:
            return self.NULL
        result: list[str] = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                result.append(self.NULL)
            else:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
        return self.SEP.join(result)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        tokens = data.split(self.SEP)
        if not tokens or tokens[0] == self.NULL:
            return None

        root  = TreeNode(int(tokens[0]))
        queue = deque([root])
        idx   = 1

        while queue and idx < len(tokens):
            node = queue.popleft()

            if tokens[idx] != self.NULL:
                node.left = TreeNode(int(tokens[idx]))
                queue.append(node.left)
            idx += 1

            if idx < len(tokens) and tokens[idx] != self.NULL:
                node.right = TreeNode(int(tokens[idx]))
                queue.append(node.right)
            idx += 1

        return root


# ──────────────────────────────────────────────────────────────────────────────
# 3. LRU Cache
#    LeetCode 146 — O(1) get & put. Classic system-design-adjacent coding question.
#    Implement with a doubly-linked list + hash map (no OrderedDict cheat).
# ──────────────────────────────────────────────────────────────────────────────
class _DLLNode:
    """Node of a doubly-linked list."""
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0):
        self.key  = key
        self.val  = val
        self.prev: Optional[_DLLNode] = None
        self.next: Optional[_DLLNode] = None


class LRUCache:
    """
    Least-Recently-Used cache with O(1) get and put.

    Strategy:
      - A hash map gives O(1) node lookup.
      - A doubly-linked list orders nodes by recency (head = MRU, tail = LRU).
      - Sentinel head & tail nodes eliminate edge-case checks.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, _DLLNode] = {}
        # Sentinels
        self.head = _DLLNode()
        self.tail = _DLLNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    # ── internal helpers ──────────────────────────────────────────────────────

    def _remove(self, node: _DLLNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: _DLLNode) -> None:
        """Insert right after the head sentinel (MRU position)."""
        node.next       = self.head.next
        node.prev       = self.head
        self.head.next.prev = node
        self.head.next      = node

    # ── public API ────────────────────────────────────────────────────────────

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._insert_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = _DLLNode(key, value)
        self.cache[key] = node
        self._insert_front(node)
        if len(self.cache) > self.capacity:
            # Evict LRU node (just before tail sentinel)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# ──────────────────────────────────────────────────────────────────────────────
# 4. Word Ladder II
#    LeetCode 126 — Find ALL shortest transformation sequences.
#    Hard: BFS for shortest distance + backtracking for path reconstruction.
# ──────────────────────────────────────────────────────────────────────────────
def find_ladders(begin_word: str, end_word: str,
                 word_list: list[str]) -> list[list[str]]:
    """
    Returns all shortest transformation sequences from begin_word to end_word,
    changing exactly one letter at a time, using only words in word_list.
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return []

    # BFS to build a parent map: word -> set of words that lead to it
    # at the shortest distance layer.
    layer: set[str]              = {begin_word}
    parents: dict[str, set[str]] = defaultdict(set)
    found = False

    while layer and not found:
        word_set -= layer          # remove visited to avoid revisiting
        next_layer: set[str] = set()
        for word in layer:
            for i in range(len(word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    candidate = word[:i] + c + word[i + 1:]
                    if candidate in word_set:
                        next_layer.add(candidate)
                        parents[candidate].add(word)
                        if candidate == end_word:
                            found = True
        layer = next_layer

    if not found:
        return []

    # Backtrack from end_word using the parent map
    results: list[list[str]] = []

    def backtrack(word: str, path: list[str]) -> None:
        if word == begin_word:
            results.append(list(reversed(path)))
            return
        for parent in parents[word]:
            path.append(parent)
            backtrack(parent, path)
            path.pop()

    backtrack(end_word, [end_word])
    return results


# ──────────────────────────────────────────────────────────────────────────────
# 5. Trapping Rain Water
#    LeetCode 42 — Two-pointer O(n) solution.
#    Asked at Amazon, Google, Microsoft in system-design and algo rounds.
# ──────────────────────────────────────────────────────────────────────────────
def trap(height: list[int]) -> int:
    """
    Two-pointer approach:
      At each step, process the side with the smaller max boundary,
      because that boundary is the binding constraint for water level.
    """
    left, right     = 0, len(height) - 1
    left_max        = right_max = 0
    water           = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water


# ──────────────────────────────────────────────────────────────────────────────
# 6. Longest Valid Parentheses
#    LeetCode 32 — O(n) stack-based solution.
#    Commonly asked at Google and Facebook.
# ──────────────────────────────────────────────────────────────────────────────
def longest_valid_parentheses(s: str) -> int:
    """
    Use a stack storing indices.
    The stack always keeps the index of the last unmatched ')' as a base.
    """
    stack = [-1]   # base sentinel
    max_len = 0

    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)   # new base
            else:
                max_len = max(max_len, i - stack[-1])

    return max_len


# ──────────────────────────────────────────────────────────────────────────────
# 7. Edit Distance (Levenshtein)
#    LeetCode 72 — Classic O(m*n) DP.
#    Asked at Amazon, Google, and Microsoft.
# ──────────────────────────────────────────────────────────────────────────────
def min_distance(word1: str, word2: str) -> int:
    """
    dp[i][j] = min operations to convert word1[:i] -> word2[:j].
    Three operations: insert, delete, replace (each costs 1).
    Space-optimised to two rows.
    """
    m, n = len(word1), len(word2)
    # Use only two rows to save space O(n) instead of O(m*n)
    prev = list(range(n + 1))

    for i in range(1, m + 1):
        curr = [i] + [0] * n
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(
                    prev[j],      # delete from word1
                    curr[j - 1],  # insert into word1
                    prev[j - 1],  # replace
                )
        prev = curr

    return prev[n]


# ──────────────────────────────────────────────────────────────────────────────
# 8. Alien Dictionary
#    LeetCode 269 (premium) — Topological sort via Kahn's BFS algorithm.
#    Asked at Facebook, Airbnb, Google.
# ──────────────────────────────────────────────────────────────────────────────
def alien_order(words: list[str]) -> str:
    """
    Derive character ordering from adjacent words, then topological-sort.
    Returns "" if the ordering is invalid (cycle detected).
    """
    # Initialise adjacency list for every character that appears
    adj: dict[str, set[str]] = {c: set() for word in words for c in word}

    # Build graph edges from adjacent word pairs
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        # If w1 is a prefix of w2 but longer → invalid input
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                adj[c1].add(c2)
                break

    # Kahn's BFS topological sort
    in_degree = {c: 0 for c in adj}
    for c in adj:
        for neighbor in adj[c]:
            in_degree[neighbor] += 1

    queue: deque[str] = deque(c for c in in_degree if in_degree[c] == 0)
    order: list[str]  = []

    while queue:
        c = queue.popleft()
        order.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return "".join(order) if len(order) == len(adj) else ""


# ──────────────────────────────────────────────────────────────────────────────
# 9. N-Queens
#    LeetCode 51 — Classic backtracking.
#    Tests ability to prune search space efficiently.
# ──────────────────────────────────────────────────────────────────────────────
def solve_n_queens(n: int) -> list[list[str]]:
    """
    Place n queens on an n×n board so none attack each other.
    Uses three sets to track occupied columns and diagonals in O(1).
    """
    results: list[list[str]] = []
    queens:  list[int]       = []   # queens[row] = col
    cols:    set[int]        = set()
    diag1:   set[int]        = set()  # row - col  (NW-SE diagonals)
    diag2:   set[int]        = set()  # row + col  (NE-SW diagonals)

    def backtrack(row: int) -> None:
        if row == n:
            board = []
            for col in queens:
                board.append("." * col + "Q" + "." * (n - col - 1))
            results.append(board)
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            # Place queen
            queens.append(col)
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            backtrack(row + 1)

            # Remove queen
            queens.pop()
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return results


# ──────────────────────────────────────────────────────────────────────────────
# 10. Sliding Window Maximum
#     LeetCode 239 — Monotonic deque O(n).
#     Asked at Google, Uber, Amazon to test knowledge of advanced data structures.
# ──────────────────────────────────────────────────────────────────────────────
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Maintain a deque of indices in decreasing order of nums value.
    The front of the deque is always the index of the current window's max.

    Invariants:
      - Deque contains only indices within the current window.
      - nums[deque[0]] >= nums[deque[1]] >= ... (monotonically decreasing).
    """
    result: list[int] = []
    dq: deque[int]    = deque()   # stores indices

    for i, val in enumerate(nums):
        # Remove indices outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Maintain decreasing order: pop smaller elements from the back
        while dq and nums[dq[-1]] < val:
            dq.pop()

        dq.append(i)

        # Window is fully formed after the first k elements
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Quick self-tests
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 1. Median of two sorted arrays
    assert find_median_sorted_arrays([1, 3], [2])          == 2.0
    assert find_median_sorted_arrays([1, 2], [3, 4])       == 2.5
    assert find_median_sorted_arrays([], [1])               == 1.0
    print("1. Median of Two Sorted Arrays        ✓")

    # 2. Serialize / Deserialize Binary Tree
    codec = Codec()
    root  = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
    data  = codec.serialize(root)
    restored = codec.deserialize(data)
    assert codec.serialize(restored) == data
    print("2. Serialize / Deserialize Binary Tree ✓")

    # 3. LRU Cache
    lru = LRUCache(2)
    lru.put(1, 1); lru.put(2, 2)
    assert lru.get(1)  == 1
    lru.put(3, 3)               # evicts key 2
    assert lru.get(2)  == -1
    lru.put(4, 4)               # evicts key 1
    assert lru.get(1)  == -1
    assert lru.get(3)  == 3
    assert lru.get(4)  == 4
    print("3. LRU Cache                           ✓")

    # 4. Word Ladder II
    ladders = find_ladders("hit", "cog",
                           ["hot", "dot", "dog", "lot", "log", "cog"])
    assert sorted(ladders) == sorted([
        ["hit", "hot", "dot", "dog", "cog"],
        ["hit", "hot", "lot", "log", "cog"],
    ])
    print("4. Word Ladder II                       ✓")

    # 5. Trapping Rain Water
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5])                     == 9
    print("5. Trapping Rain Water                 ✓")

    # 6. Longest Valid Parentheses
    assert longest_valid_parentheses("(()")    == 2
    assert longest_valid_parentheses(")()())") == 4
    assert longest_valid_parentheses("")       == 0
    print("6. Longest Valid Parentheses           ✓")

    # 7. Edit Distance
    assert min_distance("horse", "ros")    == 3
    assert min_distance("intention", "execution") == 5
    print("7. Edit Distance                       ✓")

    # 8. Alien Dictionary
    result = alien_order(["wrt", "wrf", "er", "ett", "rftt"])
    assert result == "wertf"
    assert alien_order(["z", "x"])    == "zx"
    assert alien_order(["z", "x", "z"]) == ""    # cycle
    print("8. Alien Dictionary                    ✓")

    # 9. N-Queens
    solutions = solve_n_queens(4)
    assert len(solutions) == 2
    solutions_8 = solve_n_queens(8)
    assert len(solutions_8) == 92
    print("9. N-Queens                            ✓")

    # 10. Sliding Window Maximum
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3,3,5,5,6,7]
    assert max_sliding_window([1], 1)                          == [1]
    print("10. Sliding Window Maximum             ✓")

    print("\nAll tests passed.")
