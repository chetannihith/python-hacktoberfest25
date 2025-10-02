# Maximum Data Flow Network Optimization

A Python solution to the HackerRank "Maximum Data Flow Network" problem from Amazon's Data Infrastructure Team coding challenge.

## Problem Description

As an engineer in Amazon's Data Infrastructure Team, you are tasked with optimizing how information flows through a network of processing nodes.

### Problem Statement

You are given:
- `n` processing nodes with bandwidth capabilities stored in an integer array `bandwidth`
- `streamCount` data channels that need to be connected to two processing nodes (one main, one secondary)
- Each data channel must utilize a **unique pair of nodes** for its connections

The `dataFlow` for each data channel is defined as:
```
dataFlow = bandwidth[main_node] + bandwidth[secondary_node]
```

### Objective

Find the **maximum total dataFlow** that can be achieved by optimally selecting unique pairs of connections for each data channel.

### Important Notes

- A pair of nodes `(x, y)` is unique if no other channel has selected the same pair
- However, the pairs `(x, y)` and `(y, x)` are treated as **different connections**
- It is possible to select the same node for both main and secondary connections: `(x, x)` is valid

## Examples

### Example 1
**Input:**
```
bandwidth = [5, 4, 8, 4, 7]
streamCount = 6
```

**Output:**
```
86
```

**Explanation:**

The 6 pairs of processing nodes with the highest sum of dataFlow are:
- `[3, 1]`, `[3, 5]`, `[5, 3]`, `[1, 3]`, `[5, 1]`, `[1, 1]` (Assuming 1-based indexing)

In 0-based indexing:
- `[2, 0]`, `[2, 4]`, `[4, 2]`, `[0, 2]`, `[4, 0]`, `[0, 0]`

Total dataFlow calculation:
```
13 (for [2, 0]) + 15 (for [2, 4]) + 15 (for [4, 2]) + 13 (for [0, 2]) 
+ 12 (for [4, 0]) + 18 (for [2, 2])
= 86
```

### Example 2
**Input:**
```
bandwidth = [14, 128, 8, 14]
streamCount = 4
```

**Output:**
```
626
```

**Explanation:**

The four pairs with the highest dataFlow are:
- `[2, 2]`: 128 + 128 = 256
- `[1, 2]`: 14 + 128 = 142
- `[2, 1]`: 128 + 14 = 142
- `[1, 1]`: 14 + 14 = 28 (if using 1-based) or similar high pairs

Total: 626

## Algorithm Approach

### Strategy
1. **Generate all possible pairs**: For `n` nodes, we can create `n²` pairs (including self-pairs and both directions)
2. **Calculate dataFlow for each pair**: Sum of bandwidth values for each pair
3. **Sort pairs by dataFlow**: Arrange in descending order
4. **Select top `streamCount` pairs**: Sum the highest dataFlow values

### Time Complexity
- **Generating pairs**: O(n²)
- **Sorting**: O(n² log n²) = O(n² log n)
- **Overall**: O(n² log n)

### Space Complexity
- O(n²) for storing all possible dataFlow values

## Constraints

- `1 ≤ n ≤ 2 × 10⁵`
- `1 ≤ bandwidth[i] ≤ 2 × 10⁵`
- `1 ≤ streamCount ≤ min(n², n²) = n²`

## Usage

### Running the Solution

```bash
python max_dataflow.py
```

#### Input Format
```
n
bandwidth[0]
bandwidth[1]
...
bandwidth[n-1]
streamCount
```

#### Example Input
```
5
5
4
8
4
7
6
```

#### Output
```
86
```

### Running Tests

```bash
python test_max_dataflow.py
```

The test suite includes:
- ✅ Sample test cases from HackerRank
- ✅ Edge cases (single node, minimum values)
- ✅ Uniform bandwidth values
- ✅ Large bandwidth values (up to constraints)
- ✅ Performance tests with large inputs
- ✅ Various data distributions

## Files

- `max_dataflow.py` - Main solution implementation
- `test_max_dataflow.py` - Comprehensive unit tests
- `README.md` - This documentation file

## Implementation Details

### Function Signature
```python
def determineMaxDataFlow(bandwidth: list, streamCount: int) -> int:
    """
    Args:
        bandwidth: Array of bandwidth capability for each node
        streamCount: Number of data channels to connect
    
    Returns:
        Maximum total dataFlow achievable
    """
```

### Key Points

1. **Self-pairing allowed**: A node can be paired with itself `(i, i)`
2. **Directional pairs**: `(i, j)` and `(j, i)` are different pairs
3. **Greedy approach**: Always select pairs with highest dataFlow
4. **All pairs generated**: We generate all n² possible combinations

## Contributing

This solution was created as part of Hacktoberfest 2025 contributions. Feel free to:
- Optimize the algorithm further
- Add more test cases
- Improve documentation
- Fix any bugs

## Author

Contributed to the python-hacktoberfest25 repository
Date: October 2025

## License

This project follows the same license as the parent repository.
