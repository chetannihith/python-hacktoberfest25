#!/usr/bin/env python3
"""
Comprehensive test suite for the Amazon Parcel Shipper problem.
Includes edge cases and stress tests.
"""

import unittest
from parcel_shipper import getMinUnshippedParcels, getMinUnshippedParcels_optimized


class TestParcelShipper(unittest.TestCase):
    """Test cases for the parcel shipper problem"""
    
    def test_example_case_1(self):
        """Test the main example from the problem"""
        weights = [7, 1, 7, 4]
        max_wt = 6
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 2, "Should return 2 unshipped parcels")
    
    def test_sample_case_0(self):
        """Test sample case 0"""
        weights = [5, 3, 1, 9, 7]
        max_wt = 4
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 3, "Should return 3 unshipped parcels")
    
    def test_sample_case_1(self):
        """Test sample case 1 - all parcels too heavy"""
        weights = [1, 6, 8]
        max_wt = 1
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 3, "Should return 3 unshipped parcels")
    
    # Edge Cases
    
    def test_empty_weights(self):
        """Test with empty weights array"""
        weights = []
        max_wt = 10
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 0, "Empty array should return 0")
    
    def test_single_parcel_can_ship(self):
        """Test with single parcel that can be shipped"""
        weights = [5]
        max_wt = 10
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 0, "Single parcel under capacity should ship")
    
    def test_single_parcel_cannot_ship(self):
        """Test with single parcel that cannot be shipped"""
        weights = [10]
        max_wt = 5
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 1, "Single parcel over capacity cannot ship")
    
    def test_zero_capacity(self):
        """Test with zero capacity"""
        weights = [1, 2, 3]
        max_wt = 0
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 3, "Zero capacity should ship nothing")
    
    def test_negative_capacity(self):
        """Test with negative capacity"""
        weights = [1, 2, 3]
        max_wt = -5
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 3, "Negative capacity should ship nothing")
    
    def test_all_parcels_same_weight(self):
        """Test when all parcels have the same weight"""
        weights = [5, 5, 5, 5]
        max_wt = 6
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 3, "Should ship only first parcel")
    
    def test_all_parcels_can_ship(self):
        """Test when all parcels can be shipped"""
        weights = [1, 2, 3, 4]
        max_wt = 10
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 0, "All parcels should be shipped")
    
    def test_all_parcels_cannot_ship(self):
        """Test when no parcels can be shipped"""
        weights = [10, 20, 30, 40]
        max_wt = 5
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 4, "No parcels should be shipped")
    
    def test_capacity_runs_out_midway(self):
        """Test when capacity decreases to zero midway"""
        weights = [1, 1, 1, 1, 1]
        max_wt = 3
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 3, "Should ship 2 parcels before capacity hits 1")
    
    def test_large_weights(self):
        """Test with very large weight values"""
        weights = [999999999, 1, 2]
        max_wt = 1000000000
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 0, "Should handle large numbers correctly")
    
    def test_many_small_parcels(self):
        """Test with many small parcels"""
        weights = [1] * 100
        max_wt = 50
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 51, "Should ship 49 parcels (capacity 50 to 2)")
    
    def test_alternating_weights(self):
        """Test with alternating heavy and light parcels"""
        weights = [100, 1, 100, 1, 100, 1]
        max_wt = 10
        result = getMinUnshippedParcels(weights, max_wt)
        # Should ship the three 1-weight parcels
        self.assertEqual(result, 3, "Should ship light parcels only")
    
    def test_ascending_order_input(self):
        """Test with already sorted ascending weights"""
        weights = [1, 2, 3, 4, 5]
        max_wt = 4
        result = getMinUnshippedParcels(weights, max_wt)
        # Ships: 3 (cap 4->3), 2 (cap 3->2), 1 (cap 2->1). Then 4,5 cannot ship
        self.assertEqual(result, 2, "Should handle ascending order correctly")
    
    def test_descending_order_input(self):
        """Test with already sorted descending weights"""
        weights = [5, 4, 3, 2, 1]
        max_wt = 6
        result = getMinUnshippedParcels(weights, max_wt)
        # Ships: 5 (cap 6->5), 4 (cap 5->4), 3 (cap 4->3), 2 (cap 3->2), 1 (cap 2->1)
        self.assertEqual(result, 0, "Should handle descending order correctly")
    
    def test_equal_weight_and_capacity(self):
        """Test when parcel weight equals capacity"""
        weights = [5, 5, 5]
        max_wt = 5
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 3, "Equal weight should not ship (strictly less than)")
    
    def test_optimized_version_consistency(self):
        """Test that optimized version produces same results"""
        test_cases = [
            ([7, 1, 7, 4], 6),
            ([5, 3, 1, 9, 7], 4),
            ([1, 6, 8], 1),
            ([1, 2, 3, 4, 5], 10),
            ([], 5),
        ]
        
        for weights, max_wt in test_cases:
            result1 = getMinUnshippedParcels(weights, max_wt)
            result2 = getMinUnshippedParcels_optimized(weights, max_wt)
            self.assertEqual(result1, result2, 
                           f"Both versions should match for weights={weights}, max_wt={max_wt}")


class TestPerformance(unittest.TestCase):
    """Performance tests for large inputs"""
    
    def test_large_input(self):
        """Test with maximum constraint size"""
        # Create 10^5 parcels
        weights = list(range(1, 100001))
        max_wt = 50000
        result = getMinUnshippedParcels(weights, max_wt)
        # Should ship parcels with weight < 50000, 49999, 49998, etc.
        self.assertIsInstance(result, int, "Should handle large input")
        self.assertGreaterEqual(result, 0, "Result should be non-negative")
    
    def test_all_max_weight(self):
        """Test with all parcels at maximum weight"""
        weights = [1000000000] * 1000
        max_wt = 1000000000
        result = getMinUnshippedParcels(weights, max_wt)
        self.assertEqual(result, 1000, "No parcels can ship when weight equals capacity")


if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)
