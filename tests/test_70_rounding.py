import unittest
from decimal import Decimal
from modelling_case_study import _money

class TestRounding(unittest.TestCase):
    """
    This Test Checks the Rounding Helper Function _money():
    - Rounds to 2 decimal places correctly
    - Accepts int, float and Decimal inputs
    - Returns a float (JSON-friendly)
    """

    def test_money_helper_function(self):
        # Test Ints
        self.assertEqual(_money(100), 100.00)
        self.assertEqual(_money(0), 0.00)

        # Test Floats
        self.assertEqual(_money(100.456), 100.46)
        self.assertEqual(_money(100.455), 100.46)
        self.assertEqual(_money(100.454), 100.45)

        # Test Decimals
        self.assertEqual(_money(Decimal("100.4567")), 100.46)
        self.assertEqual(_money(Decimal("100.4556")), 100.46)
        self.assertEqual(_money(Decimal("100.4544")), 100.45)


if __name__ == "__main__":
    unittest.main() 