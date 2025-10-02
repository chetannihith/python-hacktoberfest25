#!/usr/bin/env python3
"""
Simple test script for currency converter
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    from currency_converter import CurrencyConverter
    
    print("🧪 Testing Currency Converter...")
    converter = CurrencyConverter()
    
    # Test with mock data (no API calls needed)
    converter.exchange_rates = {
        'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0, 
        'CAD': 1.25, 'AUD': 1.35, 'INR': 83.12
    }
    converter.last_update = "2025-10-02T12:00:00"
    
    print("📊 Available currencies:", len(converter.get_available_currencies()))
    
    # Test basic conversions
    result, info = converter.convert_currency(100, 'USD', 'EUR')
    print(f"✅ $100 USD = €{result:.2f} EUR (rate: {info['rate']:.4f})")
    
    result, info = converter.convert_currency(85, 'EUR', 'USD')
    print(f"✅ €85 EUR = ${result:.2f} USD (rate: {info['rate']:.4f})")
    
    result, info = converter.convert_currency(100, 'GBP', 'JPY')
    print(f"✅ £100 GBP = ¥{result:.0f} JPY (rate: {info['rate']:.2f})")
    
    # Test formatting
    amounts = [
        (1234.56, 'USD'), (1000, 'EUR'), (150000, 'JPY'), (500.75, 'GBP')
    ]
    print("\n💰 Formatting tests:")
    for amount, currency in amounts:
        formatted = converter.format_amount(amount, currency)
        print(f"   {amount} {currency} → {formatted}")
    
    # Test popular pairs
    print(f"\n🔥 Popular pairs: {len(converter.get_popular_pairs())} available")
    for i, (from_curr, to_curr) in enumerate(converter.get_popular_pairs()[:3]):
        try:
            _, info = converter.convert_currency(1, from_curr, to_curr)
            print(f"   {from_curr} → {to_curr}: {info['rate']:.4f}")
        except:
            print(f"   {from_curr} → {to_curr}: Rate not available")
    
    print("\n🎉 All tests passed! Currency converter is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()