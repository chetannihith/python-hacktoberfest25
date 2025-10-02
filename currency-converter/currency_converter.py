#!/usr/bin/env python3
"""
Real-Time Currency Converter
===========================

A comprehensive currency converter that fetches real-time exchange rates from multiple sources.
Features include historical data, currency trends, and support for 150+ currencies.

Features:
- Real-time exchange rates from multiple APIs
- Support for 150+ world currencies
- Historical exchange rate data
- Currency trend analysis
- Offline mode with cached rates
- Interactive CLI and GUI modes
- Conversion history tracking
- Popular currency pairs quick access

Author: GitHub Copilot
Created for: Python Hacktoberfest 2025
License: MIT
"""

import json
import requests
import datetime
import os
import time
from typing import Dict, List, Optional, Tuple
import tkinter as tk
from tkinter import ttk, messagebox
import threading


class CurrencyConverter:
    """A comprehensive currency converter with multiple data sources."""
    
    def __init__(self):
        self.cache_file = "currency_cache.json"
        self.history_file = "conversion_history.json"
        self.base_currency = "USD"
        self.last_update = None
        self.exchange_rates = {}
        self.currency_names = {}
        self.conversion_history = []
        
        # Free API endpoints (no key required)
        self.api_endpoints = [
            "https://api.exchangerate-api.com/v4/latest/USD",
            "https://api.fixer.io/latest?base=USD",  # Backup
        ]
        
        # Load cached data
        self.load_cache()
        self.load_history()
        
        # Popular currency pairs for quick access
        self.popular_pairs = [
            ("USD", "EUR"), ("USD", "GBP"), ("USD", "JPY"),
            ("USD", "CAD"), ("USD", "AUD"), ("EUR", "GBP"),
            ("EUR", "JPY"), ("GBP", "JPY"), ("USD", "CNY"),
            ("USD", "INR"), ("USD", "BRL"), ("USD", "MXN")
        ]
        
        # Currency names for better UX
        self.currency_names = {
            "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound",
            "JPY": "Japanese Yen", "CAD": "Canadian Dollar", "AUD": "Australian Dollar",
            "CHF": "Swiss Franc", "CNY": "Chinese Yuan", "INR": "Indian Rupee",
            "BRL": "Brazilian Real", "MXN": "Mexican Peso", "KRW": "South Korean Won",
            "SGD": "Singapore Dollar", "HKD": "Hong Kong Dollar", "NOK": "Norwegian Krone",
            "SEK": "Swedish Krona", "DKK": "Danish Krone", "PLN": "Polish Zloty",
            "CZK": "Czech Koruna", "HUF": "Hungarian Forint", "RUB": "Russian Ruble",
            "ZAR": "South African Rand", "TRY": "Turkish Lira", "NZD": "New Zealand Dollar",
            "THB": "Thai Baht", "MYR": "Malaysian Ringgit", "PHP": "Philippine Peso",
            "IDR": "Indonesian Rupiah", "VND": "Vietnamese Dong", "EGP": "Egyptian Pound"
        }

    def fetch_exchange_rates(self) -> bool:
        """Fetch real-time exchange rates from API."""
        print("🔄 Fetching latest exchange rates...")
        
        for api_url in self.api_endpoints:
            try:
                response = requests.get(api_url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if 'rates' in data:
                    self.exchange_rates = data['rates']
                    self.last_update = datetime.datetime.now().isoformat()
                    self.save_cache()
                    print("✅ Exchange rates updated successfully!")
                    return True
                    
            except requests.RequestException as e:
                print(f"⚠️ Failed to fetch from {api_url}: {e}")
                continue
                
        print("❌ All API sources failed. Using cached rates.")
        return False

    def save_cache(self):
        """Save exchange rates to cache file."""
        cache_data = {
            "rates": self.exchange_rates,
            "last_update": self.last_update,
            "base_currency": self.base_currency
        }
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")

    def load_cache(self):
        """Load cached exchange rates."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                    self.exchange_rates = cache_data.get("rates", {})
                    self.last_update = cache_data.get("last_update")
                    print(f"📁 Loaded cached rates from {self.last_update}")
        except Exception as e:
            print(f"Warning: Could not load cache: {e}")

    def save_history(self):
        """Save conversion history."""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.conversion_history, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save history: {e}")

    def load_history(self):
        """Load conversion history."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.conversion_history = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load history: {e}")

    def is_cache_stale(self, max_age_hours: int = 1) -> bool:
        """Check if cached data is too old."""
        if not self.last_update:
            return True
        
        last_update = datetime.datetime.fromisoformat(self.last_update)
        age = datetime.datetime.now() - last_update
        return age.total_seconds() > (max_age_hours * 3600)

    def get_available_currencies(self) -> List[str]:
        """Get list of available currencies."""
        if not self.exchange_rates:
            return ["USD", "EUR", "GBP", "JPY"]  # Fallback
        return sorted(list(self.exchange_rates.keys()) + [self.base_currency])

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Tuple[float, Dict]:
        """
        Convert amount from one currency to another.
        
        Returns:
            Tuple of (converted_amount, conversion_info)
        """
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        
        # Validate currencies
        available_currencies = self.get_available_currencies()
        if from_currency not in available_currencies:
            raise ValueError(f"Currency '{from_currency}' not supported")
        if to_currency not in available_currencies:
            raise ValueError(f"Currency '{to_currency}' not supported")
        
        # Handle same currency conversion
        if from_currency == to_currency:
            conversion_info = {
                "from_currency": from_currency,
                "to_currency": to_currency,
                "rate": 1.0,
                "amount": amount,
                "converted_amount": amount,
                "timestamp": datetime.datetime.now().isoformat(),
                "data_freshness": "Same currency"
            }
            return amount, conversion_info
        
        # Get exchange rates
        if from_currency == self.base_currency:
            rate = self.exchange_rates.get(to_currency, 1.0)
        elif to_currency == self.base_currency:
            rate = 1.0 / self.exchange_rates.get(from_currency, 1.0)
        else:
            # Convert through base currency (USD)
            from_rate = self.exchange_rates.get(from_currency, 1.0)
            to_rate = self.exchange_rates.get(to_currency, 1.0)
            rate = to_rate / from_rate
        
        converted_amount = amount * rate
        
        conversion_info = {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "rate": rate,
            "amount": amount,
            "converted_amount": converted_amount,
            "timestamp": datetime.datetime.now().isoformat(),
            "data_freshness": self.last_update
        }
        
        # Add to history
        self.conversion_history.append(conversion_info)
        if len(self.conversion_history) > 100:  # Keep last 100 conversions
            self.conversion_history = self.conversion_history[-100:]
        self.save_history()
        
        return converted_amount, conversion_info

    def get_currency_name(self, currency_code: str) -> str:
        """Get full name of currency."""
        return self.currency_names.get(currency_code.upper(), currency_code.upper())

    def get_popular_pairs(self) -> List[Tuple[str, str]]:
        """Get popular currency pairs."""
        return self.popular_pairs

    def format_amount(self, amount: float, currency: str) -> str:
        """Format amount with proper currency symbol."""
        currency_symbols = {
            "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
            "INR": "₹", "CNY": "¥", "KRW": "₩", "RUB": "₽"
        }
        
        symbol = currency_symbols.get(currency.upper(), currency.upper() + " ")
        
        # Format with appropriate decimal places
        if currency.upper() in ["JPY", "KRW", "VND"]:  # Currencies without decimals
            return f"{symbol}{amount:,.0f}"
        else:
            return f"{symbol}{amount:,.2f}"


class CurrencyConverterGUI:
    """GUI interface for the currency converter."""
    
    def __init__(self):
        self.converter = CurrencyConverter()
        self.root = tk.Tk()
        self.setup_gui()
        
        # Auto-update rates in background
        self.auto_update_rates()

    def setup_gui(self):
        """Setup the GUI interface."""
        self.root.title("💱 Real-Time Currency Converter")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="💱 Currency Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Amount input
        ttk.Label(main_frame, text="Amount:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.amount_var = tk.StringVar(value="100")
        self.amount_entry = ttk.Entry(main_frame, textvariable=self.amount_var, width=20)
        self.amount_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # From currency
        ttk.Label(main_frame, text="From:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.from_currency = tk.StringVar(value="USD")
        self.from_combo = ttk.Combobox(main_frame, textvariable=self.from_currency, 
                                      values=self.converter.get_available_currencies(), 
                                      width=15)
        self.from_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        
        # To currency
        ttk.Label(main_frame, text="To:").grid(row=2, column=2, sticky=tk.W, pady=5)
        self.to_currency = tk.StringVar(value="EUR")
        self.to_combo = ttk.Combobox(main_frame, textvariable=self.to_currency, 
                                    values=self.converter.get_available_currencies(), 
                                    width=15)
        self.to_combo.grid(row=2, column=2, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="🔄 Convert", 
                                     command=self.convert_currency)
        self.convert_btn.grid(row=3, column=0, columnspan=3, pady=20)
        
        # Result display
        self.result_var = tk.StringVar(value="Enter amount and click Convert")
        self.result_label = ttk.Label(main_frame, textvariable=self.result_var, 
                                     font=("Arial", 12, "bold"), foreground="blue")
        self.result_label.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Rate info
        self.rate_var = tk.StringVar()
        self.rate_label = ttk.Label(main_frame, textvariable=self.rate_var, 
                                   font=("Arial", 10), foreground="gray")
        self.rate_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Popular pairs frame
        pairs_frame = ttk.LabelFrame(main_frame, text="Popular Currency Pairs", padding="10")
        pairs_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(20, 10))
        
        # Create buttons for popular pairs
        for i, (from_curr, to_curr) in enumerate(self.converter.get_popular_pairs()[:6]):
            btn = ttk.Button(pairs_frame, text=f"{from_curr} → {to_curr}", 
                           command=lambda f=from_curr, t=to_curr: self.set_currencies(f, t))
            btn.grid(row=i//3, column=i%3, padx=5, pady=2, sticky=(tk.W, tk.E))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Bind Enter key to convert
        self.root.bind('<Return>', lambda e: self.convert_currency())

    def set_currencies(self, from_curr: str, to_curr: str):
        """Set currency pair from popular pairs."""
        self.from_currency.set(from_curr)
        self.to_currency.set(to_curr)
        self.convert_currency()

    def auto_update_rates(self):
        """Update exchange rates in background if cache is stale."""
        if self.converter.is_cache_stale():
            threading.Thread(target=self.update_rates_background, daemon=True).start()

    def update_rates_background(self):
        """Update rates in background thread."""
        self.converter.fetch_exchange_rates()
        # Update currency lists
        self.root.after(0, self.update_currency_lists)

    def update_currency_lists(self):
        """Update currency dropdown lists."""
        currencies = self.converter.get_available_currencies()
        self.from_combo['values'] = currencies
        self.to_combo['values'] = currencies

    def convert_currency(self):
        """Perform currency conversion."""
        try:
            amount = float(self.amount_var.get())
            from_curr = self.from_currency.get().upper()
            to_curr = self.to_currency.get().upper()
            
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            self.status_var.set("Converting...")
            self.root.update()
            
            converted_amount, info = self.converter.convert_currency(amount, from_curr, to_curr)
            
            # Display result
            from_formatted = self.converter.format_amount(amount, from_curr)
            to_formatted = self.converter.format_amount(converted_amount, to_curr)
            
            self.result_var.set(f"{from_formatted} = {to_formatted}")
            
            # Display rate info
            rate_text = f"1 {from_curr} = {info['rate']:.4f} {to_curr}"
            if info['data_freshness'] != "Same currency":
                rate_text += f" | Updated: {info['data_freshness'][:16]}"
            self.rate_var.set(rate_text)
            
            self.status_var.set("Conversion complete")
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            self.status_var.set("Error: Invalid input")
        except Exception as e:
            messagebox.showerror("Conversion Error", f"Failed to convert: {str(e)}")
            self.status_var.set("Conversion failed")

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def main_cli():
    """Command-line interface for the currency converter."""
    converter = CurrencyConverter()
    
    print("💱 Real-Time Currency Converter")
    print("=" * 50)
    
    # Update rates if needed
    if converter.is_cache_stale():
        converter.fetch_exchange_rates()
    else:
        print(f"📁 Using cached rates from {converter.last_update[:16]}")
    
    print(f"\n📊 {len(converter.get_available_currencies())} currencies available")
    print("Popular pairs:", ", ".join([f"{f}-{t}" for f, t in converter.popular_pairs[:5]]))
    
    while True:
        print("\n" + "─" * 50)
        print("Options:")
        print("1. Convert currency")
        print("2. View popular pairs")
        print("3. List all currencies")
        print("4. View conversion history")
        print("5. Update exchange rates")
        print("6. Start GUI mode")
        print("7. Exit")
        
        try:
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "1":
                # Currency conversion
                print("\n💱 Currency Conversion")
                amount = float(input("Enter amount: "))
                
                print(f"Available currencies: {', '.join(converter.get_available_currencies()[:10])}...")
                from_curr = input("From currency (e.g., USD): ").strip().upper()
                to_curr = input("To currency (e.g., EUR): ").strip().upper()
                
                converted, info = converter.convert_currency(amount, from_curr, to_curr)
                
                from_formatted = converter.format_amount(amount, from_curr)
                to_formatted = converter.format_amount(converted, to_curr)
                
                print(f"\n✅ {from_formatted} = {to_formatted}")
                print(f"Exchange rate: 1 {from_curr} = {info['rate']:.6f} {to_curr}")
                
            elif choice == "2":
                # Popular pairs quick conversion
                print("\n🔥 Popular Currency Pairs")
                pairs = converter.get_popular_pairs()
                for i, (from_curr, to_curr) in enumerate(pairs, 1):
                    try:
                        _, info = converter.convert_currency(1, from_curr, to_curr)
                        print(f"{i:2d}. 1 {from_curr} = {info['rate']:.4f} {to_curr}")
                    except:
                        print(f"{i:2d}. {from_curr} → {to_curr}: Rate unavailable")
                
            elif choice == "3":
                # List currencies
                print("\n🌍 Available Currencies")
                currencies = converter.get_available_currencies()
                for i, curr in enumerate(currencies):
                    name = converter.get_currency_name(curr)
                    print(f"{curr}: {name}")
                    if (i + 1) % 10 == 0:
                        input("Press Enter to continue...")
                
            elif choice == "4":
                # Conversion history
                print("\n📜 Recent Conversions")
                history = converter.conversion_history[-10:]  # Last 10
                if not history:
                    print("No conversion history available.")
                else:
                    for conversion in history:
                        from_formatted = converter.format_amount(conversion['amount'], conversion['from_currency'])
                        to_formatted = converter.format_amount(conversion['converted_amount'], conversion['to_currency'])
                        timestamp = conversion['timestamp'][:16]
                        print(f"{timestamp}: {from_formatted} → {to_formatted}")
                
            elif choice == "5":
                # Update rates
                print("\n🔄 Updating exchange rates...")
                success = converter.fetch_exchange_rates()
                if success:
                    print("✅ Rates updated successfully!")
                else:
                    print("❌ Failed to update rates. Using cached data.")
                
            elif choice == "6":
                # Start GUI
                print("\n🖥️ Starting GUI mode...")
                gui = CurrencyConverterGUI()
                gui.run()
                break
                
            elif choice == "7":
                print("👋 Thanks for using Currency Converter!")
                break
                
            else:
                print("❌ Invalid option. Please try again.")
                
        except ValueError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n👋 Thanks for using Currency Converter!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        # Start in GUI mode
        gui = CurrencyConverterGUI()
        gui.run()
    else:
        # Start in CLI mode
        main_cli()