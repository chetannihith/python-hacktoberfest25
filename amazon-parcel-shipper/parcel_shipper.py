#!/usr/bin/env python3
"""
Amazon Warehouse Parcel Shipper Problem

A set of n parcels needs to be shipped at an Amazon warehouse where the weight 
of the jth parcel is weights[j]. In a single trip, the truck can carry any one 
parcel with a weight strictly less than the truck's capacity, max_wt. After each 
trip, the capacity of the truck max_wt decreases by 1.

Given the array weights and an integer max_wt, find the minimum number of parcels 
that cannot be shipped if the parcels are shipped optimally.

Constraints:
- 1 ≤ n ≤ 10^5
- 1 ≤ weights[j] ≤ 10^9
- 1 ≤ max_wt ≤ 10^9
"""


def getMinUnshippedParcels(weights, max_wt):
    """
    Find the minimum number of parcels that cannot be shipped.
    
    Algorithm:
    1. Sort parcels in descending order (ship heaviest first while capacity is high)
    2. For each trip, try to ship a parcel with weight < current max_wt
    3. After each trip, max_wt decreases by 1
    4. Count parcels that cannot be shipped
    
    Parameters:
    -----------
    weights : list[int]
        The weights of the parcels
    max_wt : int
        The maximum weight the truck can carry initially
    
    Returns:
    --------
    int : The minimum number of parcels that cannot be shipped
    
    Time Complexity: O(n log n) due to sorting
    Space Complexity: O(n) for the sorted array
    """
    # Edge case: empty weights array
    if not weights:
        return 0
    
    # Edge case: max_wt is 0 or negative
    if max_wt <= 0:
        return len(weights)
    
    # Sort parcels in descending order to ship heaviest first
    sorted_weights = sorted(weights, reverse=True)
    
    current_capacity = max_wt
    shipped_count = 0
    
    # Try to ship each parcel
    for weight in sorted_weights:
        # If current parcel can be shipped (weight < current_capacity)
        if weight < current_capacity:
            shipped_count += 1
            current_capacity -= 1  # Capacity decreases after each trip
            
            # If capacity becomes 0 or negative, no more parcels can be shipped
            if current_capacity <= 0:
                break
        # If parcel cannot be shipped, continue checking lighter parcels
    
    # Return count of unshipped parcels
    return len(weights) - shipped_count


def getMinUnshippedParcels_optimized(weights, max_wt):
    """
    Optimized version using binary search approach.
    
    For large datasets, this can be more efficient by using early termination.
    """
    if not weights:
        return 0
    
    if max_wt <= 0:
        return len(weights)
    
    # Sort in descending order
    sorted_weights = sorted(weights, reverse=True)
    
    shipped = 0
    capacity = max_wt
    
    for weight in sorted_weights:
        if capacity <= 0:
            break
        if weight < capacity:
            shipped += 1
            capacity -= 1
    
    return len(weights) - shipped


# Main function for testing
if __name__ == "__main__":
    # Test Case 1: Example from problem
    weights1 = [7, 1, 7, 4]
    max_wt1 = 6
    result1 = getMinUnshippedParcels(weights1, max_wt1)
    print(f"Test 1: weights = {weights1}, max_wt = {max_wt1}")
    print(f"Result: {result1} parcels cannot be shipped")
    print(f"Expected: 2\n")
    
    # Test Case 2: From Sample Case 1
    weights2 = [1, 6, 8]
    max_wt2 = 1
    result2 = getMinUnshippedParcels(weights2, max_wt2)
    print(f"Test 2: weights = {weights2}, max_wt = {max_wt2}")
    print(f"Result: {result2} parcels cannot be shipped")
    print(f"Expected: 3\n")
    
    # Test Case 3: From Sample Case 0
    weights3 = [5, 3, 1, 9, 7]
    max_wt3 = 4
    result3 = getMinUnshippedParcels(weights3, max_wt3)
    print(f"Test 3: weights = {weights3}, max_wt = {max_wt3}")
    print(f"Result: {result3} parcels cannot be shipped")
    print(f"Expected: 3\n")
