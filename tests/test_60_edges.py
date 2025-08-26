import unittest
from decimal import Decimal
from copy import deepcopy
from modelling_case_study import get_example_data, rate_hull_for_drone, rate_tpl_for_drone, rate_cameras, apply_camera_extension, apply_drone_extension, compute_totals

# Helpers for Consistent Rounding
Q2 = Decimal("0.01")  # 2 Decimal Places

def D(x):
    """
    Helper to convert numbers to Decimal safely. 
    """
    return x if isinstance(x, Decimal) else Decimal(str(x))


class TestEdgeCases(unittest.TestCase):
    """
    This Test Checks Edge Cases across the model:
    - Zero Values
    - Unknown Weight Values
    - Extension Edge Cases
    """
    
    def test_zero_drones(self):
        """
        1) Zero Drones
        - After the extensions are applied, all camera premiums should be £50. 
        - (No. of drones = 0, no 'top n' so all cameras are extras).
        """

        model_data = get_example_data()
        model_data["drones"] = []

        rate_cameras(model_data)
        apply_camera_extension(model_data)
        compute_totals(model_data)

        # All camera premiums should be £50
        camera_premiums = [D(cam["hull_premium"]) for cam in model_data["detachable_cameras"]]
        self.assertTrue(len(camera_premiums) > 0)
        self.assertTrue(all(premium == D("50.00") for premium in camera_premiums))

        # Drone premiums should be None
        self.assertEqual(model_data["net_prem"]["drones_hull"], D("0"))
        self.assertEqual(model_data["net_prem"]["drones_tpl"], D("0"))

    
    def test_zero_cameras(self):
        """
        2) Zero Cameras
        - Camera totals should be £0 and no crash.
        """

        model_data = get_example_data()
        model_data["detachable_cameras"] = []

        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
            rate_tpl_for_drone(drone)

        # No cameras to rate but extensions and totals should still work
        rate_cameras(model_data)
        apply_drone_extension(model_data)
        apply_camera_extension(model_data)
        compute_totals(model_data)

        self.assertEqual(D(model_data["net_prem"]["cameras_hull"]), D("0"))

    
    def test_max_drones_in_air_limit(self):
        """
        3) Max Drones in Air Limit
        - Test to ensure that if max_drones_in_air is equal to the number of drones, there is no change in drone expected premiums. 
        - (i.e. all drones are 'top n' so no drone is an extra).
        """

        model_data = get_example_data()
        num_drones = len(model_data["drones"])
        model_data["max_drones_in_air"] = num_drones

        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
            rate_tpl_for_drone(drone)

        apply_drone_extension(model_data)

        # Expected results (serial -> (factor, final_rate, premium))
        expected = {
            "AAA-111": D("600.00"),    # 10000 * 0.06 
            "BBB-222": D("1152.00"),   # 12000 * 0.096
            "AAA-123": D("1080.00"),   # 15000 * 0.072
        }

        # Drone premiums should be unchanged
        for drone in model_data["drones"]:
            serial_n = drone["serial_number"]
            self.assertEqual(D(drone["hull_premium"]).quantize(Q2), expected[serial_n].quantize(Q2))

    
    def test_minimum_drones_in_air_limit(self):
        """
        4) Minimum Drones in Air Limit
        - Test to ensure that if max_drones_in_air is set to 0, no drones get the full premium.
        - (i.e. all drones are 'extras' so all drone premiums are set to £150).
        """

        model_data = get_example_data()
        model_data["max_drones_in_air"] = 0

        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
            rate_tpl_for_drone(drone)

        apply_drone_extension(model_data)

        # Drone premiums should be as expected
        for drone in model_data["drones"]:
            self.assertEqual(D(drone["hull_premium"]).quantize(Q2), D("150.00"))

    
    def test_one_more_camera_than_drones(self):
        """
        5) More Cameras than Drones
        - Test to ensure that if there are more cameras than drones, the correct number of cameras get the full premium and the rest are extras.
        - (already tested in test_30_cameras but this is an explicit edge case).
        """

        model_data = get_example_data()
        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
            rate_tpl_for_drone(drone)
        
        rate_cameras(model_data)
        apply_camera_extension(model_data)

        # There are 3 drones, so 3 cameras should be full premium, 1 camera should be £50
        flat_rate_cameras = [cam for cam in model_data["detachable_cameras"] if D(cam["hull_premium"]) == D("50.00")]
        self.assertEqual(len(flat_rate_cameras), 1)

    
    def test_equal_cameras_and_drones(self):
        """
        6) Equal Cameras and Drones
        - Test to ensure that if there are equal cameras and drones, all cameras get the full premium.
        - (i.e. no cameras are extras).
        """

        model_data = get_example_data()
        model_data["detachable_cameras"] = model_data["detachable_cameras"][:len(model_data["drones"])]

        for drone in model_data["drones"]:
            rate_hull_for_drone(drone)
            rate_tpl_for_drone(drone)

        rate_cameras(model_data)
        apply_camera_extension(model_data)

        # None of the cameras should be flat rate
        flat_rate_cameras = [cam for cam in model_data["detachable_cameras"] if D(cam["hull_premium"]) == D("50.00")]
        self.assertEqual(len(flat_rate_cameras), 0)

    
    def test_unknown_weight_drone(self):
        """
        7) Unknown Weight Drone
        - Test to ensure if a drone has an invalid weight band, an error is raised.
        """

        model_data = get_example_data()
        model_data = deepcopy(model_data)
        model_data["drones"][0]["weight"] = "30 - 50kg" # Invalid weight band

        with self.assertRaises((KeyError, ValueError)):
            for drone in model_data["drones"]:
                rate_hull_for_drone(drone)

        
if __name__ == "__main__":
    unittest.main()
