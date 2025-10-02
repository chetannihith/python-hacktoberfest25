import unittest
from main import check_password_strength

class TestPasswordStrength(unittest.TestCase):
    def test_very_strong(self):
        pw = "HarshDubeySun42!"
        level, feedback = check_password_strength(pw)
        self.assertEqual(level, "Very Strong 💪")

    def test_weak(self):
        pw = "abc123"
        level, feedback = check_password_strength(pw)
        self.assertEqual(level, "Weak ❌")

if __name__ == "__main__":
    unittest.main()
