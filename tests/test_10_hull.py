import unittest
from decimal import Decimal
from modelling_case_study import get_example_data, rate_hull_for_drone

# Helpers for Consistent Rounding
Q2 = Decimal("0.01")  # 2 Decimal Places
Q4 = Decimal("0.0001")  # 4 Decimal Places

def D(x):
    """
    Helper to convert numbers to Decimal safely. 
    """
    return x if isinstance(x, Decimal) else Decimal(str(x))


class TestDroneHull(unittest.TestCase):
    """
    This Test Checks:
    - Base hull rate: 0.06
    - Weight adjustment per band: 1.0/1.2/1.6
    - Premium per drone: value * (base * factor), rounded to 2dp
    """

    def test_per_drone_fields_and_premiums(self):
        model_data = get_example_data()
        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)

        # Expected results (serial -> (factor, final_rate, premium))
        expected = {
            "AAA-111": (D("1.0"), D("0.0600"), D("600.00")),    # 10000 * 0.06 
            "BBB-222": (D("1.6"), D("0.0960"), D("1152.00")),   # 12000 * 0.096
            "AAA-123": (D("1.2"), D("0.0720"), D("1080.00")),   # 15000 * 0.072
        }

        for drone in model_data["drones"]:
            serial_n = drone["serial_number"]

            # Base Rate Matches
            self.assertEqual(D(drone["hull_base_rate"]).quantize(Q4), D("0.0600"))

            # Factor, Final Rate & Premium Match
            self.assertEqual(D(drone["hull_weight_adjustment"]).quantize(Q4), expected[serial_n][0].quantize(Q4))
            self.assertEqual(D(drone["hull_final_rate"]).quantize(Q4), expected[serial_n][1].quantize(Q4))
            self.assertEqual(D(drone["hull_premium"]).quantize(Q2), expected[serial_n][2].quantize(Q2))

    def test_total_hull_premium(self):
        model_data = get_example_data()
        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
        
        total_premium = sum(D(drone["hull_premium"]) for drone in model_data["drones"])
        self.assertEqual(total_premium.quantize(Q2), D("2832.00"))
        

if __name__ == "__main__":
    unittest.main()