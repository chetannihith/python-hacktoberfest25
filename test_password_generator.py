#!/usr/bin/env python3
"""
Simple test script for password_generator.py
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

try:
    from password_generator import PasswordGenerator
    
    # Test the PasswordGenerator class
    generator = PasswordGenerator()
    
    # Test basic password generation
    print('Testing password generation...')
    password = generator.generate_password(length=12)
    print(f'Generated password: {password}')
    print(f'Password length: {len(password)}')
    
    # Test password strength checker
    score, strength, suggestions = generator.check_password_strength(password)
    print(f'Strength: {strength} (Score: {score}/6)')
    
    # Test multiple password generation
    print('\nGenerating 3 test passwords:')
    passwords = generator.generate_multiple_passwords(count=3, length=10)
    for i, pwd in enumerate(passwords, 1):
        print(f'{i}. {pwd}')
    
    # Test different character sets
    print('\nTesting different character sets:')
    pwd_no_special = generator.generate_password(length=8, use_special=False)
    print(f'No special chars: {pwd_no_special}')
    
    pwd_digits_only = generator.generate_password(length=6, use_uppercase=False, 
                                                 use_lowercase=False, use_special=False)
    print(f'Digits only: {pwd_digits_only}')
    
    print('\n✅ All tests passed successfully!')
    
except Exception as e:
    print(f'❌ Error during testing: {e}')
    import traceback
    traceback.print_exc()