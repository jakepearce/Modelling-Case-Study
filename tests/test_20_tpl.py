import unittest
from decimal import Decimal
from modelling_case_study import get_example_data, rate_tpl_for_drone

# Helpers for Consistent Rounding
Q2 = Decimal("0.01")  # 2 Decimal Places
Q4 = Decimal("0.0001")  # 4 Decimal Places

def D(x):
    """
    Helper to convert numbers to Decimal safely. 
    """
    return x if isinstance(x, Decimal) else Decimal(str(x))

class TestDroneTPL(unittest.TestCase):
    """
    This Test Checks:
    - Base TPL rate = 0.02
    - ILFs used across the three drones = 1.00, 0.53, 0.31
    - Each drone has:
        tpl_base_rate, tpl_base_layer_premium, tpl_ilf, tpl_layer_premium
    - Money rounded per drone to 2dp
    """

    def test_fields_and_calculation_consistency(self):
        model_data = get_example_data()
        for drone in model_data["drones"]:
            rate_tpl_for_drone(drone)

        for drone in model_data["drones"]:
            
            # 1) Check fields exist
            self.assertIn("tpl_base_rate", drone)
            self.assertIn("tpl_base_layer_premium", drone)
            self.assertIn("tpl_ilf", drone)
            self.assertIn("tpl_layer_premium", drone)

            # 2) Test base rate is 2%
            self.assertEqual(D(drone["tpl_base_rate"]).quantize(Q4), D("0.0200"))

            # 3) Test layer premium = base_layer_premium * ilf (rounded to 2dp)
            calc = (D(drone["tpl_base_layer_premium"]) * D(drone["tpl_ilf"])).quantize(Q2)
            self.assertEqual(D(drone["tpl_layer_premium"]).quantize(Q2), calc)

    
    def test_total_and_expected_ilfs(self):
        model_data = get_example_data()
        for drone in model_data["drones"]:
            rate_tpl_for_drone(drone)

        # Total Net for TPL
        total = sum(D(drone["tpl_layer_premium"]) for drone in model_data["drones"])
        self.assertEqual(total.quantize(Q2), D("420.20"))

        # ILFs match expected
        ilfs = [D(drone["tpl_ilf"]).quantize(Q2) for drone in model_data["drones"]]
        self.assertCountEqual(ilfs, [D("1.00"), D("0.53"), D("0.31")])

if __name__ == "__main__":
    unittest.main()
