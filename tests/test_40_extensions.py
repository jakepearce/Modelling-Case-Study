import unittest
from decimal import Decimal
from modelling_case_study import get_example_data, rate_hull_for_drone, rate_tpl_for_drone, rate_cameras, apply_drone_extension, apply_camera_extension
from tests.test_helpers import D, Q2


class TestExtensions(unittest.TestCase):
    """
    Test 1 Checks:
    - Set max_drones_in_air = 1 so only the most expensive drone stays at full hull premium. 
    - All other drones get a flat hull premium of £150.
    - Check individual drones and total hull premium. 
    """
    def test_drones_extension(self):
        model_data = get_example_data()
        model_data["max_drones_in_air"] = 1  # Set to 1 for this test
        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
            rate_tpl_for_drone(drone)
        
        apply_drone_extension(model_data)

        # 1) Check individual drones (most expensive premium is £1152)
        premiums = sorted([D(drone["hull_premium"]).quantize(Q2) for drone in model_data["drones"]])
        self.assertEqual(premiums, [D("150.00"), D("150.00"), D("1152.00")])

        # 2) Check total hull premium (1152 + 150 + 150 = 1452)
        total_premium = sum(D(drone["hull_premium"]) for drone in model_data["drones"])
        self.assertEqual(total_premium.quantize(Q2), D("1452.00"))

    """
    Test 2 Checks:
    - With 4 cameras and 3 drones (but only a maximum of two in the air), two should become £50. 
    - The calculated highest hull rate is 0.072. 
    - Check individual cameras and total camera hull premium.
    """
    def test_cameras_extension(self):
        model_data = get_example_data()
        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
        
        rate_cameras(model_data)
        apply_camera_extension(model_data)

        # 1) Check individual cameras
        premiums = sorted([D(cam["hull_premium"]).quantize(Q2) for cam in model_data["detachable_cameras"]])
        self.assertEqual(premiums, [D("50.00"), D("50.00"), D("180.00"), D("360.00")])

        # 2) Check total camera hull premium (360 + 180 + 50 + 50 = 640)
        total_premium = sum(D(cam["hull_premium"]) for cam in model_data["detachable_cameras"])
        self.assertEqual(total_premium.quantize(Q2), D("640.00"))


if __name__ == "__main__":
    unittest.main()





