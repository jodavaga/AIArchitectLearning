import unittest
from main import calculate_pi


class TestPiCalculation(unittest.TestCase):
    """Test cases for the calculate_pi function"""
    
    def test_pi_to_5_digits(self):
        """Test that pi is calculated correctly to 5 decimal places"""
        result = calculate_pi(5)
        expected = 3.14159
        # Check if the result matches pi to 5 decimal places
        self.assertAlmostEqual(result, expected, places=5)
    
    def test_pi_first_digit(self):
        """Test that the integer part is correct"""
        result = calculate_pi(5)
        self.assertEqual(int(result), 3)
    
    def test_pi_range(self):
        """Test that pi is in the expected range"""
        result = calculate_pi(5)
        self.assertGreater(result, 3.14159)
        self.assertLess(result, 3.14160)
    
    def test_pi_string_representation(self):
        """Test the string representation starts correctly"""
        result = calculate_pi(5)
        result_str = f"{result:.5f}"
        self.assertTrue(result_str.startswith("3.14159"))
    
    def test_different_precision(self):
        """Test calculation with different precision"""
        result_3 = calculate_pi(3)
        result_7 = calculate_pi(7)
        # Both should be close to pi
        self.assertAlmostEqual(result_3, 3.14159, places=3)
        self.assertAlmostEqual(result_7, 3.14159, places=5)


if __name__ == '__main__':
    print("Testing pi calculation function...")
    print(f"Pi to 5 digits: {calculate_pi(5)}")
    print(f"Expected value: 3.14159...")
    print("\nRunning unit tests:")
    unittest.main()
