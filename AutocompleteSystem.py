import heapq
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = {}
        self.freq_map = defaultdict(int)  # word -> frequency
        self.is_end = False

class AutocompleteSystem:
    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word, freq=1):
        """Add or update a word with given frequency"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.freq_map[word] += freq
        node.is_end = True
        print(f"Added/Updated word '{word}' with frequency {freq}")

    def input(self, prefix):
        """Return top 3 most frequent words with given prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # use max heap to get top 3
        heap = [(-freq, word) for word, freq in node.freq_map.items()]
        heapq.heapify(heap)
        suggestions = []
        for _ in range(min(3, len(heap))):
            freq, word = heapq.heappop(heap)
            suggestions.append(word)
        return suggestions


# 🔹 Example Usage
auto = AutocompleteSystem()
auto.add_word("dog", 5)
auto.add_word("dove", 3)
auto.add_word("door", 7)
auto.add_word("dodge", 2)
auto.add_word("cat", 6)

print("\nTop suggestions for 'do':", auto.input("do"))
print("Top suggestions for 'd':", auto.input("d"))
print("Top suggestions for 'c':", auto.input("c"))
print("Top suggestions for 'z':", auto.input("z"))
