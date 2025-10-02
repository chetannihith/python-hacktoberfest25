# robust_password_checker.py
"""
Advanced Password Strength Checker 🔐
------------------------------------
Evaluates the strength of any password and provides detailed improvement suggestions.
"""

import re

def check_password_strength(password):
    feedback = []

    # Length evaluation
    length = len(password)
    if length >= 16:
        length_score = 3
    elif length >= 12:
        length_score = 2
        feedback.append("Consider making it longer for extra security (16+ characters).")
    elif length >= 8:
        length_score = 1
        feedback.append("Password is short; consider using 12+ characters.")
    else:
        length_score = 0
        feedback.append("Password is too short; use at least 8 characters.")

    # Character variety
    upper = bool(re.search(r"[A-Z]", password))
    lower = bool(re.search(r"[a-z]", password))
    digit = bool(re.search(r"[0-9]", password))
    special = bool(re.search(r"[!@#$%^&*?_]", password))

    variety_score = upper + lower + digit + special
    if not upper:
        feedback.append("Add at least one uppercase letter.")
    if not lower:
        feedback.append("Add at least one lowercase letter.")
    if not digit:
        feedback.append("Add at least one number.")
    if not special:
        feedback.append("Add at least one special character (!@#$%^&*?_).")

    # Check for repeated sequences or common patterns
    common_patterns = ["123", "abc", "password", "qwerty", "letmein", "admin"]
    pattern_flag = False
    for pattern in common_patterns:
        if pattern.lower() in password.lower():
            feedback.append(f"Avoid common pattern: '{pattern}'.")
            pattern_flag = True
    repeat_flag = bool(re.search(r"(.)\1{2,}", password))
    if repeat_flag:
        feedback.append("Avoid repeated characters (e.g., 'aaa', '111').")

    # Calculate overall score
    score = length_score + variety_score
    if pattern_flag or repeat_flag:
        score -= 1  # Penalize if weak patterns detected

    # Determine strength
    if score >= 7:
        level = "Very Strong 💪"
    elif score >= 5:
        level = "Strong 👍"
    elif score >= 3:
        level = "Medium ⚠️"
    else:
        level = "Weak ❌"

    return level, feedback

def main():
    print("🔐 Advanced Password Strength Checker 🔐")
    password = input("Enter any password to check: ").strip()

    level, feedback = check_password_strength(password)
    print(f"\nPassword Strength: {level}")
    if feedback:
        print("Suggestions to improve:")
        for f in feedback:
            print(f" - {f}")

if __name__ == "__main__":
    main()
