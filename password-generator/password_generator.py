import random
import string
from typing import List


def generate_password(
    length: int, use_uppercase: bool, use_numbers: bool, use_symbols: bool
) -> str:
    """
    Generates a secure, random password based on specified criteria.

    Args:
        length: The desired length of the password.
        use_uppercase: Whether to include uppercase letters.
        use_numbers: Whether to include numbers.
        use_symbols: Whether to include special symbols.

    Returns:
        A randomly generated password string.
    """
    char_pool: str = string.ascii_lowercase
    password_chars: List[str] = []

    # Build the character pool and guarantee at least one of each required type
    if use_uppercase:
        char_pool += string.ascii_uppercase
        password_chars.append(random.choice(string.ascii_uppercase))

    if use_numbers:
        char_pool += string.digits
        password_chars.append(random.choice(string.digits))

    if use_symbols:
        char_pool += string.punctuation
        password_chars.append(random.choice(string.punctuation))

    # Fill the rest of the password length with random characters from the pool
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(random.choice(char_pool))

    # Shuffle the list to ensure guaranteed characters are not always at the start
    random.shuffle(password_chars)

    return "".join(password_chars)


if __name__ == "__main__":
    print("--- Secure Password Generator ---")

    try:
        pass_length = int(input("Enter desired password length (min 8): ").strip())
        if pass_length < 8:
            print("Password length is too short. Setting to minimum of 8.")
            pass_length = 8

        include_uppercase = (
            input("Include uppercase letters? (y/n): ").strip().lower() == "y"
        )
        include_numbers = input("Include numbers? (y/n): ").strip().lower() == "y"
        include_symbols = input("Include special symbols? (y/n): ").strip().lower() == "y"

        if not (include_uppercase or include_numbers or include_symbols):
            print("Warning: Generating a password with only lowercase letters.")

        # Generate and display the password
        new_password = generate_password(
            pass_length, include_uppercase, include_numbers, include_symbols
        )
        print("\n" + "=" * 20)
        print(f"Generated Password: {new_password}")
        print("=" * 20)

    except ValueError:
        print("Invalid input. Please enter a valid number for the length.")
    except Exception as e:
        print(f"An error occurred: {e}")