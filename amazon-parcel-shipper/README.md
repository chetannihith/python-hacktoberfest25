# Amazon Warehouse Parcel Shipper Problem

## Problem Description

A set of `n` parcels needs to be shipped at an Amazon warehouse where the weight of the *j*th parcel is `weights[j]`. In a single trip, the truck can carry any one parcel with a weight **strictly less than** the truck's capacity, `max_wt`. After each trip, the capacity of the truck `max_wt` decreases by 1.

Given the array `weights` and an integer `max_wt`, find the **minimum number of parcels that cannot be shipped** if the parcels are shipped optimally.

### Constraints
- `1 ≤ n ≤ 10^5`
- `1 ≤ weights[j] ≤ 10^9`
- `1 ≤ max_wt ≤ 10^9`

## Solution Approach

### Algorithm
The optimal strategy is to ship the heaviest parcels first while the truck's capacity is high:

1. **Sort parcels in descending order** (heaviest first)
2. **Greedy selection**: For each trip, ship a parcel if its weight is strictly less than the current capacity
3. **Decrease capacity**: After each successful trip, reduce `max_wt` by 1
4. **Count unshipped**: Return the count of parcels that couldn't be shipped

### Time Complexity
- **O(n log n)** - dominated by the sorting operation
- **O(n)** - for the shipping simulation

### Space Complexity
- **O(n)** - for the sorted array

## Examples

### Example 1
```python
weights = [7, 1, 7, 4]
max_wt = 6
# Output: 2
```

**Explanation:**
- Trip 1: Ship parcel with weight 4 (capacity 6 → 5)
- Trip 2: Ship parcel with weight 1 (capacity 5 → 4)
- Remaining parcels [7, 7] cannot be shipped (both ≥ 4)
- **Result: 2 parcels unshipped**

### Example 2
```python
weights = [5, 3, 1, 9, 7]
max_wt = 4
# Output: 3
```

**Explanation:**
- Trip 1: Ship parcel with weight 3 (capacity 4 → 3)
- Trip 2: Ship parcel with weight 1 (capacity 3 → 2)
- Remaining parcels [5, 9, 7] cannot be shipped (all ≥ 2)
- **Result: 3 parcels unshipped**

### Example 3
```python
weights = [1, 6, 8]
max_wt = 1
# Output: 3
```

**Explanation:**
- No parcel weighs less than 1
- **Result: 3 parcels unshipped**

## Usage

### Running the Solution
```bash
python parcel_shipper.py
```

### Running Tests
```bash
python test_parcel_shipper.py
```

Or with verbose output:
```bash
python -m unittest test_parcel_shipper -v
```

## Test Coverage

The test suite includes:

### Basic Test Cases
- Example cases from the problem
- Sample test cases

### Edge Cases
- Empty weights array
- Single parcel scenarios
- Zero or negative capacity
- All parcels same weight
- All parcels can/cannot ship
- Capacity runs out midway
- Very large weight values
- Equal weight and capacity

### Stress Tests
- Large input size (10^5 parcels)
- Maximum weight values (10^9)
- Performance validation

## Files

- `parcel_shipper.py` - Main solution implementation
- `test_parcel_shipper.py` - Comprehensive test suite
- `README.md` - This documentation

## Key Insights

1. **Greedy Strategy**: Shipping heaviest parcels first is optimal because:
   - Heavy parcels can only be shipped when capacity is high
   - Light parcels can potentially be shipped later
   
2. **Strictly Less Than**: The condition `weight < capacity` (not `≤`) is crucial:
   - If weight equals capacity, it cannot be shipped
   
3. **Decreasing Capacity**: After each trip, capacity decreases by 1:
   - This creates urgency to ship heavy items first
   - Eventually, capacity may reach a point where no parcels can be shipped

## Contributing

This solution was created as part of Hacktoberfest 2025 contributions. Feel free to:
- Add more test cases
- Optimize the algorithm further
- Improve documentation
- Add visualizations

## Author

Created for the python-hacktoberfest25 repository.
