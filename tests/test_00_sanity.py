import unittest
from modelling_case_study import main

class TestSanity(unittest.TestCase):
    """
    This test checks only:
    - main() returns something (and that it's a Dict)
    - the top-level keys relied upon are present
    - Key types are correct (lists/dicts).
    """
    
    def test_main_returns_structure(self):

        model_data = main()

        # 1) Basic Type: Expect a Dictionary
        self.assertIsInstance(model_data, dict)

        # 2) Required Top-Level Keys Exist
        for key in ("drones", "detachable_cameras", "net_prem", "gross_prem"):
            self.assertIn(key, model_data, f"Missing top-level key: {key}")

        # 3) Key Types
        self.assertIsInstance(model_data["drones"], list)
        self.assertIsInstance(model_data["detachable_cameras"], list)
        self.assertIsInstance(model_data["net_prem"], dict)
        self.assertIsInstance(model_data["gross_prem"], dict)

if __name__ == "__main__":
    unittest.main()