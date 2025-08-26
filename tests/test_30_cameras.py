import unittest
from decimal import Decimal
from modelling_case_study import get_example_data, rate_hull_for_drone, rate_cameras
from tests.test_helpers import D, Q2, Q4


class TestCameraHull(unittest.TestCase):
    """
    This Test Checks:
    - Hull rates match highest eligible rate: 0.0720
    - Individual camera premiums calculated correctly
    - Total camera hull premium is correct
    """

    def test_camera_rate(self):
        model_data = get_example_data()
        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
        
        rate_cameras(model_data)

        # All Cameras should have a rate of 0.0720, matching the highest rate drone (AAA-123)
        for cam in model_data["detachable_cameras"]:
            self.assertEqual(D(cam["hull_rate"]).quantize(Q4), D("0.0720"))

    
    def test_individual_camera_premiums(self):
        model_data = get_example_data()
        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
        
        rate_cameras(model_data)

        # Highest eligible drone hull rate = 0.0720
        # Premiums should = value * 0.072, rounded per camera to 2dp. 
        expected = {
            "ZZZ-999": D("360.00"),     # 5000 * 0.072
            "YYY-888": D("180.00"),     # 2500 * 0.072
            "XXX-777": D("108.00"),     # 1500 * 0.072
            "WWW-666": D("144.00"),     # 2000 * 0.072
        }
        
        for cam in model_data["detachable_cameras"]:
            self.assertIn(cam["serial_number"], expected)
            self.assertEqual(D(cam["hull_rate"]).quantize(Q4), D("0.0720"))
            self.assertEqual(D(cam["hull_premium"]).quantize(Q2), expected[cam["serial_number"]])


    def test_total_camera_hull_premium(self):
        model_data = get_example_data()
        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
        
        rate_cameras(model_data)

        total_premium = sum(D(cam["hull_premium"]) for cam in model_data["detachable_cameras"])
        self.assertEqual(total_premium.quantize(Q2), D("792.00"))


if __name__ == "__main__":
    unittest.main()