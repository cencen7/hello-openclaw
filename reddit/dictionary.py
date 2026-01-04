"""
given a series of words dictionary, determine是否可以有一个序列可以连接上。 
如果有这样的一个path，需要让我们判断是否可以找到这个path。
每次可以转换1个或者2个character。
这里面可以用深度搜索和广度搜索，但其实并不容易，因为还要考虑2个character的情况。面试考察coding是不容易的。


Graph Interpretation

Each word is a node

An edge exists between two words if their Hamming distance is 1 or 2

The problem becomes:
Is there a path from start to end in this graph?

"""

"""
This is a Word-Ladder-style problem where words are nodes, 
edges connect words with Hamming distance 1 or 2, 
and we use BFS to determine whether the start word can reach the end word.

High-Level BFS Logic (Interview-Friendly)

- Put start into a queue
- Mark it as visited
- While the queue is not empty:
    - Take one word
    - Generate all dictionary words that differ by 1 or 2 characters
    - Add unvisited ones to the queue

- If we reach end, return true
- If BFS finishes without reaching end, return false
"""
from typing import List
from collections import deque, defaultdict
from itertools import combinations


def hamming_distance(word1, word2):
    distance = 0
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            distance += 1
    return distance
            

def exsits_transform_path1(start: str, end: str, word_list: List[str]) -> bool:
    """
    return true if there exsits a seq of transformations from start to end
    where each step changes 1 or 2 chars and the intermediate word must be in word_list.
    Otherwise, return False

    n words
    l len(start)
    this implementation has time complexity high: O(n**2 * L); space compleixty of O(n)
    """
    if len(start) != len(end):
        return False
    
    # if edit distance is <= 2
    if hamming_distance(start, end) <=2:
        return True
   
    # if end not in word_list:
    word_set = set(word_list)
    if end not in word_set: 
        return False
    
    # set up visited and queue
    visited = set()
    queue = deque()

    # initalize with start
    queue.append(start)
    visited.add(start)

    while len(queue) > 0:
        cur = queue.popleft()
        if cur == end:
            return True
        # find all words within hammingtom distance <=2
        for word in word_list:
            if hamming_distance(cur, word) <= 2:
                if word not in visited:
                    queue.append(word)
                    visited.add(word)

    return False


def exsits_transform_path2(start: str, end: str, word_list: List[str]) -> bool:
    """
    return true if there exsits a seq of transformations from start to end
    where each step changes 1 or 2 chars and the intermediate word must be in word_list.
    Otherwise, return False

    n words
    l len(start)
    this implementation has time complexity high: O(n * L); space compleixty of O(n * L)
    """
    if len(start) != len(end):
        return False
    
    # if edit distance is <= 2
    if hamming_distance(start, end) <=2:
        return True
    
    # if end not in word_list:
    word_set = set(word_list)
    if end not in word_set: 
        return False
    
    # build pattern buckets
    # map1: one-star patterns --> words
    map1 = defaultdict(list)
    for w in word_list:
        for i in range(len(start)):
            p1 = w[:i] + "*" + w[i+1:]
            map1[p1].append(w)


    # build pattern buckets
    # map2: two-star patterns --> words
    map2 = defaultdict(list)
    for w in word_list:
        for i in range(len(start)):
            for j in range(i+1, len(start)):
                p2 = w[:i] + "*" + w[i+1:j] + "*" + w[j+1:]
                map2[p2].append(w)

    # print(f"map1: {map1}")
    # print(f"map2: {map2}")

    # set up visited and queue
    visited = set()
    queue = deque()

    # initalize with start
    queue.append(start)
    visited.add(start)
    parent = {}

    while len(queue) > 0:
        cur = queue.popleft()
        if cur == end:
            path = []
            while cur in parent:
                path.append(cur)
                cur = parent[cur]
            path.append(start)
            path.reverse()
            print("path is:", path)
            return True
        
        # print(f"visiting {cur}====")
        
        # 1-char neighbors
        for i in range(len(cur)):
            cur_pattern1 = cur[:i] + "*" + cur[i+1:]
            if cur_pattern1 in map1:
                for w in map1[cur_pattern1]:
                    if w not in visited:
                        queue.append(w)
                        visited.add(w)
                        parent[w] = cur
        
        # 2-char neighbors
        for i in range(len(cur)):
            for j in range(i+1, len(cur)):
                cur_pattern2 = cur[:i] + "*" + cur[i+1:j] + "*" + cur[j+1:]
                if cur_pattern2 in map2:
                    for w in map2[cur_pattern2]:
                        if w not in visited:
                            queue.append(w)
                            visited.add(w)
                            parent[w] = cur
        
    return False


def exists_transform_path(
    start: str,
    end: str,
    word_list: List[str],
    max_diff: int = 2,
) -> bool:
    """
    Return True if there exists a sequence of transformations from start to end,
    where each step changes 1..max_diff characters (Hamming distance),
    and every intermediate word (and end) must be in word_list.

    Also prints one valid path when found.
    """
    if max_diff < 1:
        raise ValueError("max_diff must be >= 1")

    if len(start) != len(end):
        return False

    if start == end:
        print("path is:", [start])
        return True

    word_set = set(word_list)
    if end not in word_set:
        return False

    L = len(start)

    # Optional early exit: direct jump allowed
    if hamming_distance(start, end) <= max_diff:
        print("path is:", [start, end])
        return True

    # -------------------------
    # Build wildcard pattern buckets:
    # pattern_maps[d][pattern] -> list of words matching that pattern
    # where pattern has exactly d '*' chars
    # -------------------------
    # Include start too, in case start isn't in word_list (common in interview)
    all_words = word_set | {start}

    pattern_maps = [None] + [defaultdict(list) for _ in range(max_diff)]  # index 1..max_diff
    for w in all_words:
        for d in range(1, max_diff + 1):
            for idxs in combinations(range(L), d):
                chars = list(w)
                for i in idxs:
                    chars[i] = "*"
                pattern = "".join(chars)
                pattern_maps[d][pattern].append(w)

    # -------------------------
    # BFS + parent map to reconstruct path
    # -------------------------
    q = deque([start])
    visited = set([start])
    parent = {}  # parent[child] = previous_word

    while q:
        cur = q.popleft()
        if cur == end:
            # reconstruct path
            path = []
            node = end
            while node in parent:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            print("path is:", path)
            return True

        # generate neighbors via patterns of size 1..max_diff
        for d in range(1, max_diff + 1):
            for idxs in combinations(range(L), d):
                chars = list(cur)
                for i in idxs:
                    chars[i] = "*"
                pattern = "".join(chars)

                for nxt in pattern_maps[d].get(pattern, []):
                    if nxt in visited:
                        continue
                    # safety filter (usually redundant but keeps it correct)
                    dist = hamming_distance(cur, nxt)
                    if 1 <= dist <= max_diff:
                        visited.add(nxt)
                        parent[nxt] = cur
                        q.append(nxt)

    return False

def run_tests():
    tests = [
        ("abcd", "wxyz", ["abcd", "abyd", "wxyz"], False),
        ("same", "same", [], True),
        ("same", "sam", [], False),
        ("cold", "warm", [], False),
        ("cold", "warm", ["cold", "cord", "ward", "warm"], True),
        ("cold", "warm", ["cold", "gold", "goad", "load"], False),
        ("same", "same", ["same", "came", "lame"], True),
        ("cold", "warm", ["cold", "cord", "card", "ward"], False),
        ("abcd", "abef", ["abcd", "abef"], True),
        ("cold", "warm", [], False),
        (
            "aaaa",
            "bbbb",
            [
                "aaaa",
                "aaab", "aaba", "abaa", "baaa",
                "aabb", "abab", "abba", "baab", "baba", "bbaa",
                "abbb", "babb", "bbab", "bbba",
                "bbbb",
            ],
            True
        ),
    ]
    for i, (start, end, word_list, expected) in enumerate(tests):
        result = exists_transform_path(start, end, word_list, max_diff=2)
        print(f'ran test case {i}: start: {start}; end: {end}; world_list: {word_list}: got: {result}; expected: {expected}')
        assert result == expected, f"Test {i} failed: got {result}, expected {expected}"
    

if __name__ == '__main__':
    run_tests()


