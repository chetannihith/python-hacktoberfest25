import heapq
from collections import defaultdict

class LibrarySystem:
    def __init__(self, entries):
        """
        entries: List of [branchId, bookId, price]
        """
        self.available_books = defaultdict(list)   # bookId -> min-heap of (price, branchId)
        self.rented_books = []                     # global min-heap of (price, branchId, bookId)
        self.price_map = {}                        # (branchId, bookId) -> price
        self.invalid_available = set()             # lazy deletion markers
        self.invalid_rented = set()

        for branch, book, price in entries:
            self.price_map[(branch, book)] = price
            heapq.heappush(self.available_books[book], (price, branch, book))

    def search(self, bookId):
        """Return up to 5 cheapest branches where this book is available."""
        result = []
        if bookId in self.available_books:
            temp = []
            while self.available_books[bookId] and (self.available_books[bookId][0] in self.invalid_available):
                heapq.heappop(self.available_books[bookId])

            for _ in range(5):
                if not self.available_books[bookId]:
                    break
                price, branch, book = heapq.heappop(self.available_books[bookId])
                result.append(branch)
                temp.append((price, branch, book))

            # push back for future queries
            for item in temp:
                heapq.heappush(self.available_books[bookId], item)

        return result

    def rent(self, branch, book):
        """Rent a book: move from available -> rented."""
        price = self.price_map[(branch, book)]
        entry = (price, branch, book)

        # Mark as removed from available
        self.invalid_available.add(entry)

        # Add to rented heap
        heapq.heappush(self.rented_books, entry)

    def drop(self, branch, book):
        """Return a book: move from rented -> available."""
        price = self.price_map[(branch, book)]
        entry = (price, branch, book)

        # Mark as removed from rented
        self.invalid_rented.add(entry)

        # Add back to available
        heapq.heappush(self.available_books[book], entry)

    def report(self):
        """Return up to 5 cheapest rented books as [branch, book]."""
        result = []
        while self.rented_books and (self.rented_books[0] in self.invalid_rented):
            heapq.heappop(self.rented_books)

        temp = []
        for _ in range(5):
            if not self.rented_books:
                break
            price, branch, book = heapq.heappop(self.rented_books)
            result.append([branch, book])
            temp.append((price, branch, book))

        # push back
        for item in temp:
            heapq.heappush(self.rented_books, item)

        return result


# Example usage:
entries = [
    [1, 101, 5],   # branch 1 has book 101 at price 5
    [2, 101, 4],   # branch 2 has book 101 at price 4
    [3, 102, 7],
    [1, 103, 6],
    [2, 104, 2]
]

ls = LibrarySystem(entries)

print("Search book 101:", ls.search(101))  # expect [2, 1]
ls.rent(2, 101)
print("Report after renting:", ls.report())  # expect [[2, 101]]
ls.drop(2, 101)
print("Report after drop:", ls.report())  # expect []
