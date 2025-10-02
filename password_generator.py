#!/usr/bin/env python3
"""
Password Generator Tool
=======================

A secure password generator that creates customizable passwords with various character sets.
Perfect for generating strong passwords for your accounts.

Features:
- Customizable password length
- Include/exclude uppercase letters, lowercase letters, numbers, and special characters
- Generate multiple passwords at once
- Copy to clipboard functionality
- Password strength indicator

Author: GitHub Copilot
Created for: Python Hacktoberfest 2025
"""

import random
import string
import secrets
import pyperclip


class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def generate_password(self, length=12, use_uppercase=True, use_lowercase=True, 
                         use_digits=True, use_special=True, exclude_ambiguous=False):
        """
        Generate a secure password with specified criteria.
        
        Args:
            length (int): Length of the password (default: 12)
            use_uppercase (bool): Include uppercase letters
            use_lowercase (bool): Include lowercase letters
            use_digits (bool): Include digits
            use_special (bool): Include special characters
            exclude_ambiguous (bool): Exclude ambiguous characters (0, O, l, 1, etc.)
        
        Returns:
            str: Generated password
        """
        if length < 4:
            raise ValueError("Password length should be at least 4 characters")
        
        # Build character set
        chars = ""
        
        if use_lowercase:
            chars += self.lowercase
        if use_uppercase:
            chars += self.uppercase
        if use_digits:
            chars += self.digits
        if use_special:
            chars += self.special_chars
            
        if not chars:
            raise ValueError("At least one character type must be selected")
        
        # Remove ambiguous characters if requested
        if exclude_ambiguous:
            ambiguous = "0O1lI"
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        # Generate password ensuring at least one character from each selected type
        password = []
        
        # Ensure at least one character from each selected type
        if use_lowercase:
            password.append(secrets.choice(self.lowercase))
        if use_uppercase:
            password.append(secrets.choice(self.uppercase))
        if use_digits:
            password.append(secrets.choice(self.digits))
        if use_special:
            password.append(secrets.choice(self.special_chars))
        
        # Fill the rest of the password
        for _ in range(length - len(password)):
            password.append(secrets.choice(chars))
        
        # Shuffle the password to avoid predictable patterns
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def generate_multiple_passwords(self, count=5, **kwargs):
        """Generate multiple passwords with the same criteria."""
        return [self.generate_password(**kwargs) for _ in range(count)]
    
    def check_password_strength(self, password):
        """
        Check the strength of a password.
        
        Returns:
            tuple: (strength_score, strength_text, suggestions)
        """
        score = 0
        suggestions = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            suggestions.append("Use at least 8 characters (12+ recommended)")
        
        # Character type checks
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in self.special_chars for c in password)
        
        if has_lower:
            score += 1
        else:
            suggestions.append("Include lowercase letters")
            
        if has_upper:
            score += 1
        else:
            suggestions.append("Include uppercase letters")
            
        if has_digit:
            score += 1
        else:
            suggestions.append("Include numbers")
            
        if has_special:
            score += 1
        else:
            suggestions.append("Include special characters")
        
        # Determine strength
        if score >= 6:
            strength = "Very Strong"
        elif score >= 4:
            strength = "Strong"
        elif score >= 3:
            strength = "Moderate"
        elif score >= 2:
            strength = "Weak"
        else:
            strength = "Very Weak"
            
        return score, strength, suggestions


def main():
    """Main function to run the password generator interactively."""
    generator = PasswordGenerator()
    
    print("🔐 Password Generator Tool")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Generate a single password")
        print("2. Generate multiple passwords")
        print("3. Check password strength")
        print("4. Exit")
        
        try:
            choice = input("\nSelect an option (1-4): ").strip()
            
            if choice == "1":
                # Get password criteria
                length = int(input("Password length (default 12): ") or "12")
                
                print("\nCharacter types to include:")
                use_upper = input("Uppercase letters? (Y/n): ").lower() != 'n'
                use_lower = input("Lowercase letters? (Y/n): ").lower() != 'n'
                use_digits = input("Numbers? (Y/n): ").lower() != 'n'
                use_special = input("Special characters? (Y/n): ").lower() != 'n'
                exclude_ambiguous = input("Exclude ambiguous characters (0,O,1,l)? (y/N): ").lower() == 'y'
                
                # Generate password
                password = generator.generate_password(
                    length=length,
                    use_uppercase=use_upper,
                    use_lowercase=use_lower,
                    use_digits=use_digits,
                    use_special=use_special,
                    exclude_ambiguous=exclude_ambiguous
                )
                
                print(f"\n🔑 Generated Password: {password}")
                
                # Check strength
                score, strength, _ = generator.check_password_strength(password)
                print(f"💪 Strength: {strength} ({score}/6)")
                
                # Copy to clipboard
                try:
                    pyperclip.copy(password)
                    print("📋 Password copied to clipboard!")
                except:
                    print("📋 Could not copy to clipboard (install pyperclip for this feature)")
                
            elif choice == "2":
                count = int(input("How many passwords to generate (default 5): ") or "5")
                length = int(input("Password length (default 12): ") or "12")
                
                passwords = generator.generate_multiple_passwords(count=count, length=length)
                
                print(f"\n🔑 Generated {count} passwords:")
                for i, pwd in enumerate(passwords, 1):
                    score, strength, _ = generator.check_password_strength(pwd)
                    print(f"{i:2d}. {pwd} ({strength})")
                
            elif choice == "3":
                password = input("Enter password to check: ")
                score, strength, suggestions = generator.check_password_strength(password)
                
                print(f"\n💪 Password Strength: {strength} ({score}/6)")
                if suggestions:
                    print("💡 Suggestions for improvement:")
                    for suggestion in suggestions:
                        print(f"   - {suggestion}")
                else:
                    print("✅ Great password!")
                
            elif choice == "4":
                print("👋 Thanks for using Password Generator!")
                break
                
            else:
                print("❌ Invalid option. Please try again.")
                
        except ValueError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n👋 Thanks for using Password Generator!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    main()