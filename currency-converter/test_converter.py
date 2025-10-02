#!/usr/bin/env python3
"""
Test suite for the Currency Converter application.
Tests various functionality including conversions, error handling, and caching.
"""

import unittest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock
import sys
import threading
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from currency_converter import CurrencyConverter


class TestCurrencyConverter(unittest.TestCase):
    """Test cases for the CurrencyConverter class."""
    
    def setUp(self):
        """Set up test fixtures with temporary files."""
        # Create temporary files for testing
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, "test_cache.json")
        self.history_file = os.path.join(self.temp_dir, "test_history.json")
        
        # Create converter with test files
        self.converter = CurrencyConverter()
        self.converter.cache_file = self.cache_file
        self.converter.history_file = self.history_file
        
        # Set up test exchange rates
        self.test_rates = {
            "EUR": 0.85,
            "GBP": 0.73,
            "JPY": 110.0,
            "CAD": 1.25,
            "AUD": 1.35
        }
        self.converter.exchange_rates = self.test_rates
        self.converter.last_update = "2025-10-02T12:00:00"
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_same_currency_conversion(self):
        """Test conversion between same currencies."""
        amount = 100
        result, info = self.converter.convert_currency(amount, "USD", "USD")
        
        self.assertEqual(result, amount)
        self.assertEqual(info["rate"], 1.0)
        self.assertEqual(info["from_currency"], "USD")
        self.assertEqual(info["to_currency"], "USD")
    
    def test_usd_to_foreign_conversion(self):
        """Test conversion from USD to foreign currency."""
        amount = 100
        result, info = self.converter.convert_currency(amount, "USD", "EUR")
        
        expected = amount * self.test_rates["EUR"]
        self.assertAlmostEqual(result, expected, places=4)
        self.assertEqual(info["rate"], self.test_rates["EUR"])
    
    def test_foreign_to_usd_conversion(self):
        """Test conversion from foreign currency to USD."""
        amount = 100
        result, info = self.converter.convert_currency(amount, "EUR", "USD")
        
        expected = amount / self.test_rates["EUR"]
        self.assertAlmostEqual(result, expected, places=4)
        self.assertAlmostEqual(info["rate"], 1/self.test_rates["EUR"], places=4)
    
    def test_foreign_to_foreign_conversion(self):
        """Test conversion between two foreign currencies."""
        amount = 100
        result, info = self.converter.convert_currency(amount, "EUR", "GBP")
        
        # EUR -> USD -> GBP
        expected_rate = self.test_rates["GBP"] / self.test_rates["EUR"]
        expected = amount * expected_rate
        
        self.assertAlmostEqual(result, expected, places=4)
        self.assertAlmostEqual(info["rate"], expected_rate, places=4)
    
    def test_invalid_currency_error(self):
        """Test error handling for invalid currencies."""
        with self.assertRaises(ValueError):
            self.converter.convert_currency(100, "USD", "INVALID")
        
        with self.assertRaises(ValueError):
            self.converter.convert_currency(100, "INVALID", "EUR")
    
    def test_negative_amount_handling(self):
        """Test handling of negative amounts."""
        # Should work (absolute values)
        result, info = self.converter.convert_currency(-100, "USD", "EUR")
        self.assertEqual(result, -100 * self.test_rates["EUR"])
    
    def test_zero_amount_handling(self):
        """Test handling of zero amount."""
        result, info = self.converter.convert_currency(0, "USD", "EUR")
        self.assertEqual(result, 0)
    
    def test_currency_name_lookup(self):
        """Test currency name lookup functionality."""
        self.assertEqual(self.converter.get_currency_name("USD"), "US Dollar")
        self.assertEqual(self.converter.get_currency_name("EUR"), "Euro")
        self.assertEqual(self.converter.get_currency_name("UNKNOWN"), "UNKNOWN")
    
    def test_format_amount(self):
        """Test amount formatting with currency symbols."""
        # Test USD formatting
        formatted = self.converter.format_amount(1234.56, "USD")
        self.assertIn("$", formatted)
        self.assertIn("1,234.56", formatted)
        
        # Test JPY formatting (no decimals)
        formatted = self.converter.format_amount(1234.56, "JPY")
        self.assertIn("¥", formatted)
        self.assertIn("1,235", formatted)  # Rounded
    
    def test_popular_pairs(self):
        """Test popular currency pairs functionality."""
        pairs = self.converter.get_popular_pairs()
        self.assertIsInstance(pairs, list)
        self.assertTrue(len(pairs) > 0)
        
        # Check that pairs are tuples of strings
        for pair in pairs:
            self.assertIsInstance(pair, tuple)
            self.assertEqual(len(pair), 2)
            self.assertIsInstance(pair[0], str)
            self.assertIsInstance(pair[1], str)
    
    def test_cache_save_and_load(self):
        """Test cache saving and loading functionality."""
        # Save cache
        self.converter.save_cache()
        self.assertTrue(os.path.exists(self.cache_file))
        
        # Create new converter and load cache
        new_converter = CurrencyConverter()
        new_converter.cache_file = self.cache_file
        new_converter.load_cache()
        
        self.assertEqual(new_converter.exchange_rates, self.test_rates)
        self.assertEqual(new_converter.last_update, "2025-10-02T12:00:00")
    
    def test_history_save_and_load(self):
        """Test conversion history functionality."""
        # Perform some conversions
        self.converter.convert_currency(100, "USD", "EUR")
        self.converter.convert_currency(50, "GBP", "JPY")
        
        # Check history was recorded
        self.assertEqual(len(self.converter.conversion_history), 2)
        
        # Save and reload
        self.converter.save_history()
        new_converter = CurrencyConverter()
        new_converter.history_file = self.history_file
        new_converter.load_history()
        
        self.assertEqual(len(new_converter.conversion_history), 2)
    
    def test_cache_staleness_check(self):
        """Test cache staleness detection."""
        import datetime
        
        # Fresh cache (should not be stale)
        self.converter.last_update = datetime.datetime.now().isoformat()
        self.assertFalse(self.converter.is_cache_stale(max_age_hours=1))
        
        # Old cache (should be stale)
        old_time = datetime.datetime.now() - datetime.timedelta(hours=2)
        self.converter.last_update = old_time.isoformat()
        self.assertTrue(self.converter.is_cache_stale(max_age_hours=1))
        
        # No cache (should be stale)
        self.converter.last_update = None
        self.assertTrue(self.converter.is_cache_stale())
    
    def test_available_currencies(self):
        """Test getting available currencies."""
        currencies = self.converter.get_available_currencies()
        self.assertIsInstance(currencies, list)
        self.assertIn("USD", currencies)
        self.assertIn("EUR", currencies)
        self.assertIn("GBP", currencies)
        
        # Should be sorted
        self.assertEqual(currencies, sorted(currencies))
    
    @patch('requests.get')
    def test_fetch_exchange_rates_success(self, mock_get):
        """Test successful API rate fetching."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "rates": {"EUR": 0.85, "GBP": 0.73}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.converter.fetch_exchange_rates()
        
        self.assertTrue(result)
        self.assertEqual(self.converter.exchange_rates["EUR"], 0.85)
        self.assertEqual(self.converter.exchange_rates["GBP"], 0.73)
    
    @patch('requests.get')
    def test_fetch_exchange_rates_failure(self, mock_get):
        """Test API failure handling."""
        # Mock API failure
        mock_get.side_effect = Exception("Network error")
        
        result = self.converter.fetch_exchange_rates()
        self.assertFalse(result)
    
    def test_case_insensitive_currencies(self):
        """Test that currency codes are case-insensitive."""
        amount = 100
        
        # Test various case combinations
        result1, _ = self.converter.convert_currency(amount, "usd", "eur")
        result2, _ = self.converter.convert_currency(amount, "USD", "EUR")
        result3, _ = self.converter.convert_currency(amount, "Usd", "Eur")
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
    
    def test_large_amount_conversion(self):
        """Test conversion with very large amounts."""
        large_amount = 1_000_000_000  # 1 billion
        result, info = self.converter.convert_currency(large_amount, "USD", "EUR")
        
        expected = large_amount * self.test_rates["EUR"]
        self.assertAlmostEqual(result, expected, places=2)
    
    def test_small_amount_conversion(self):
        """Test conversion with very small amounts."""
        small_amount = 0.01  # 1 cent
        result, info = self.converter.convert_currency(small_amount, "USD", "EUR")
        
        expected = small_amount * self.test_rates["EUR"]
        self.assertAlmostEqual(result, expected, places=6)
    
    def test_conversion_info_structure(self):
        """Test that conversion info contains all required fields."""
        result, info = self.converter.convert_currency(100, "USD", "EUR")
        
        required_fields = [
            "from_currency", "to_currency", "rate", "amount",
            "converted_amount", "timestamp", "data_freshness"
        ]
        
        for field in required_fields:
            self.assertIn(field, info)
        
        # Test data types
        self.assertIsInstance(info["rate"], (int, float))
        self.assertIsInstance(info["amount"], (int, float))
        self.assertIsInstance(info["converted_amount"], (int, float))
        self.assertIsInstance(info["timestamp"], str)


class TestPerformance(unittest.TestCase):
    """Performance tests for the currency converter."""
    
    def setUp(self):
        self.converter = CurrencyConverter()
        self.converter.exchange_rates = {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0}
    
    def test_conversion_performance(self):
        """Test that conversions are fast enough."""
        start_time = time.time()
        
        # Perform 1000 conversions
        for _ in range(1000):
            self.converter.convert_currency(100, "USD", "EUR")
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        # Should complete 1000 conversions in less than 1 second
        self.assertLess(elapsed, 1.0)
    
    def test_memory_usage(self):
        """Test that memory usage stays reasonable."""
        import sys
        
        # Get initial memory usage
        initial_size = sys.getsizeof(self.converter)
        
        # Perform many conversions to build history
        for i in range(200):
            self.converter.convert_currency(i, "USD", "EUR")
        
        # Check that memory didn't grow too much
        final_size = sys.getsizeof(self.converter)
        growth = final_size - initial_size
        
        # Memory growth should be reasonable (less than 10KB for 200 conversions)
        self.assertLess(growth, 10000)


def run_comprehensive_test():
    """Run a comprehensive test of the currency converter."""
    print("🧪 Running Currency Converter Test Suite")
    print("=" * 50)
    
    # Create a test converter
    converter = CurrencyConverter()
    
    # Test basic functionality
    print("1. Testing basic conversion...")
    try:
        result, info = converter.convert_currency(100, "USD", "USD")
        assert result == 100, "Same currency conversion failed"
        print("   ✅ Same currency conversion: PASSED")
    except Exception as e:
        print(f"   ❌ Same currency conversion: FAILED ({e})")
    
    # Test with mock data
    print("2. Testing with mock exchange rates...")
    converter.exchange_rates = {"EUR": 0.85, "GBP": 0.73, "JPY": 110.0}
    
    try:
        result, info = converter.convert_currency(100, "USD", "EUR")
        expected = 100 * 0.85
        assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
        print("   ✅ USD to EUR conversion: PASSED")
    except Exception as e:
        print(f"   ❌ USD to EUR conversion: FAILED ({e})")
    
    try:
        result, info = converter.convert_currency(100, "EUR", "USD")
        expected = 100 / 0.85
        assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
        print("   ✅ EUR to USD conversion: PASSED")
    except Exception as e:
        print(f"   ❌ EUR to USD conversion: FAILED ({e})")
    
    # Test error handling
    print("3. Testing error handling...")
    try:
        converter.convert_currency(100, "USD", "INVALID")
        print("   ❌ Invalid currency test: FAILED (should have raised error)")
    except ValueError:
        print("   ✅ Invalid currency test: PASSED")
    except Exception as e:
        print(f"   ❌ Invalid currency test: FAILED (wrong error type: {e})")
    
    # Test formatting
    print("4. Testing amount formatting...")
    try:
        formatted = converter.format_amount(1234.56, "USD")
        assert "$" in formatted and "1,234.56" in formatted
        print("   ✅ USD formatting: PASSED")
        
        formatted = converter.format_amount(1234.56, "JPY")
        assert "¥" in formatted and "1,235" in formatted
        print("   ✅ JPY formatting: PASSED")
    except Exception as e:
        print(f"   ❌ Amount formatting: FAILED ({e})")
    
    # Test performance
    print("5. Testing performance...")
    try:
        start_time = time.time()
        for _ in range(1000):
            converter.convert_currency(100, "USD", "EUR")
        elapsed = time.time() - start_time
        
        if elapsed < 1.0:
            print(f"   ✅ Performance test: PASSED ({elapsed:.3f}s for 1000 conversions)")
        else:
            print(f"   ⚠️ Performance test: SLOW ({elapsed:.3f}s for 1000 conversions)")
    except Exception as e:
        print(f"   ❌ Performance test: FAILED ({e})")
    
    print("\n🎉 Test suite completed!")
    print("For detailed unit tests, run: python -m unittest test_converter.py")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--comprehensive":
        run_comprehensive_test()
    else:
        unittest.main()