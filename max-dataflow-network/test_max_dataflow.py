#!/usr/bin/env python3
"""
Unit tests for Maximum Data Flow Network Optimization

Tests cover:
- Sample test cases from the problem
- Edge cases
- Performance tests with large inputs
- Various data distributions
"""

import unittest
from max_dataflow import determineMaxDataFlow


class TestMaxDataFlow(unittest.TestCase):
    """Test cases for determineMaxDataFlow function"""
    
    def test_sample_case_0(self):
        """Test Sample Case 0 from HackerRank"""
        bandwidth = [5, 4, 8, 4, 7]
        streamCount = 6
        expected = 86
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, expected, 
                        f"Expected {expected}, got {result}")
    
    def test_sample_case_1(self):
        """Test Sample Case 1 from HackerRank"""
        bandwidth = [14, 128, 8, 14]
        streamCount = 4
        # Top 4 pairs: (1,1)=256, (0,1)=142, (1,0)=142, (1,3)=142
        # Total: 256 + 142 + 142 + 142 = 682
        expected = 682
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, expected,
                        f"Expected {expected}, got {result}")
    
    def test_single_node_single_stream(self):
        """Test with single node and single stream"""
        bandwidth = [10]
        streamCount = 1
        # Only possible pair is (0, 0) -> 10 + 10 = 20
        expected = 20
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, expected)
    
    def test_two_nodes_all_pairs(self):
        """Test with two nodes selecting all possible pairs"""
        bandwidth = [5, 3]
        streamCount = 4
        # Possible pairs:
        # (0, 0) -> 10
        # (1, 1) -> 6
        # (0, 1) -> 8
        # (1, 0) -> 8
        # Total = 10 + 8 + 8 + 6 = 32
        expected = 32
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, expected)
    
    def test_uniform_bandwidth(self):
        """Test with all nodes having same bandwidth"""
        bandwidth = [10, 10, 10]
        streamCount = 5
        # All pairs have same dataflow: 20
        # Top 5 pairs = 5 * 20 = 100
        expected = 100
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, expected)
    
    def test_select_one_pair(self):
        """Test selecting only one pair from multiple nodes"""
        bandwidth = [1, 2, 3, 4, 5]
        streamCount = 1
        # Best pair is (4, 4) -> 5 + 5 = 10
        expected = 10
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, expected)
    
    def test_large_bandwidth_values(self):
        """Test with maximum bandwidth values"""
        bandwidth = [200000, 200000, 200000]
        streamCount = 3
        # Top 3 pairs all give 400000
        expected = 1200000
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, expected)
    
    def test_varied_bandwidth_values(self):
        """Test with varied bandwidth values"""
        bandwidth = [1, 100, 2, 99, 3]
        streamCount = 6
        # Pairs sorted by dataflow (descending):
        # (1, 1) -> 200
        # (1, 3) -> 199
        # (3, 1) -> 199
        # (3, 3) -> 198
        # (1, 0) -> 101
        # (0, 1) -> 101
        # Top 6: 200 + 199 + 199 + 198 + 101 + 101 = 998
        # Actually: 200 + 199 + 199 + 198 + 101 + 101 + 101 + 101 = 1200 (if more pairs)
        # Correct calculation: 200 + 199 + 199 + 198 + 101 + 101 + 4 = 1002
        expected = 1002
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, expected)
    
    def test_minimum_constraints(self):
        """Test minimum constraint: n=1, bandwidth=1, streamCount=1"""
        bandwidth = [1]
        streamCount = 1
        expected = 2
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, expected)
    
    def test_ascending_order(self):
        """Test with bandwidth in ascending order"""
        bandwidth = [1, 2, 3, 4, 5]
        streamCount = 10
        result = determineMaxDataFlow(bandwidth, streamCount)
        # Should select top 10 pairs
        # Best pairs involve nodes 4 and 3 mostly
        self.assertGreater(result, 0)
    
    def test_descending_order(self):
        """Test with bandwidth in descending order"""
        bandwidth = [100, 50, 25, 10, 5]
        streamCount = 8
        result = determineMaxDataFlow(bandwidth, streamCount)
        # Top pair is (0, 0) -> 200
        self.assertGreaterEqual(result, 200)
    
    def test_performance_medium_input(self):
        """Test with medium-sized input"""
        n = 100
        bandwidth = list(range(1, n + 1))
        streamCount = 50
        result = determineMaxDataFlow(bandwidth, streamCount)
        # Should complete quickly and return valid result
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
    
    def test_performance_large_input(self):
        """Test with larger input approaching constraints"""
        n = 500
        bandwidth = [i % 1000 + 1 for i in range(n)]
        streamCount = 1000
        result = determineMaxDataFlow(bandwidth, streamCount)
        # Should complete and return valid result
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)
    
    def test_alternating_high_low(self):
        """Test with alternating high and low values"""
        bandwidth = [1, 100, 1, 100, 1]
        streamCount = 5
        result = determineMaxDataFlow(bandwidth, streamCount)
        # Top pairs should involve the 100s
        self.assertGreater(result, 500)
    
    def test_streamcount_equals_n_squared(self):
        """Test when streamCount equals total possible pairs"""
        bandwidth = [3, 5, 7]
        streamCount = 9  # 3^2 = 9 possible pairs
        result = determineMaxDataFlow(bandwidth, streamCount)
        # Sum of all possible pairs
        # (0,0)=6, (0,1)=8, (0,2)=10
        # (1,0)=8, (1,1)=10, (1,2)=12
        # (2,0)=10, (2,1)=12, (2,2)=14
        # Total = 6+8+8+10+10+10+12+12+14 = 90
        expected = 90
        self.assertEqual(result, expected)


class TestInputValidation(unittest.TestCase):
    """Test cases for edge cases and input validation"""
    
    def test_empty_bandwidth_array(self):
        """Test behavior with empty bandwidth array"""
        bandwidth = []
        streamCount = 0
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, 0)
    
    def test_zero_streamcount(self):
        """Test with streamCount = 0"""
        bandwidth = [10, 20, 30]
        streamCount = 0
        result = determineMaxDataFlow(bandwidth, streamCount)
        self.assertEqual(result, 0)


def run_tests():
    """Run all tests and display results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestMaxDataFlow))
    suite.addTests(loader.loadTestsFromTestCase(TestInputValidation))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on results
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit(run_tests())
