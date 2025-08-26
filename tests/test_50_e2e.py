import unittest
from decimal import Decimal
from modelling_case_study import main

# Helpers for Consistent Rounding
Q2 = Decimal("0.01")  # 2 Decimal Places

def D(x):
    """
    Helper to convert numbers to Decimal safely. 
    """
    return x if isinstance(x, Decimal) else Decimal(str(x))


class TestEndToEnd(unittest.TestCase):
    """
    This Test Checks the Expected Final Totals from the Spreadsheet are met:
    - Drone Hull NET:      2832.00 / GROSS: 4045.71
    - Drone TPL NET:        420.20 / GROSS: 600.29
    - Camera Hull NET:      792.00 / GROSS: 1131.43
    - TOTAL NET:           4044.20 / GROSS: 5777.43
    """

    def test_final_totals(self):
        model_data = main()

        # 1) Drone Hull
        self.assertEqual(D(model_data["net_prem"]["drones_hull"]).quantize(Q2), D("2832.00"))
        self.assertEqual(D(model_data["gross_prem"]["drones_hull"]).quantize(Q2), D("4045.71"))

        # 2) Drone TPL
        self.assertEqual(D(model_data["net_prem"]["drones_tpl"]).quantize(Q2), D("420.20"))
        self.assertEqual(D(model_data["gross_prem"]["drones_tpl"]).quantize(Q2), D("600.29"))

        # 3) Camera Hull
        self.assertEqual(D(model_data["net_prem"]["cameras_hull"]).quantize(Q2), D("792.00"))
        self.assertEqual(D(model_data["gross_prem"]["cameras_hull"]).quantize(Q2), D("1131.43"))

        # 4) TOTAL
        self.assertEqual(D(model_data["net_prem"]["total"]).quantize(Q2), D("4044.20"))
        self.assertEqual(D(model_data["gross_prem"]["total"]).quantize(Q2), D("5777.43"))


if __name__ == "__main__":
    unittest.main()