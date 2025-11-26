import unittest
import importlib.util
import sys

# Load the module from the file path
spec = importlib.util.spec_from_file_location("rke2_versions", "rke2-versions.py")
rke2_versions = importlib.util.module_from_spec(spec)
sys.modules["rke2_versions"] = rke2_versions
spec.loader.exec_module(rke2_versions)

get_ordered_data = rke2_versions.get_ordered_data

class TestRKE2Versions(unittest.TestCase):
    def test_channel_sorting(self):
        # Unsorted channel data, simulating an unpredictable API response
        mock_data = {
            "data": [
                {"name": "v1.20"},
                {"name": "stable"},
                {"name": "v1.2"},
                {"name": "latest"},
                {"name": "v1.10"},
                {"name": "testing"},
            ]
        }

        # The expected order: special channels first, then versions sorted semantically
        expected_order = ["stable", "latest", "testing", "v1.20", "v1.10", "v1.2"]

        ordered_data = get_ordered_data(mock_data["data"])
        ordered_names = [d["name"] for d in ordered_data]

        self.assertEqual(ordered_names, expected_order)

if __name__ == '__main__':
    unittest.main()
