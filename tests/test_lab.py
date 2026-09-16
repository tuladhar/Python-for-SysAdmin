import unittest

from syseng_lab.network import describe_subnet
from syseng_lab.system import collect_system_info, disk_usage


class SystemTests(unittest.TestCase):
    def test_system_info_contains_python_version(self):
        info = collect_system_info()
        self.assertTrue(info.python_version)
        self.assertIsInstance(info.as_dict(), dict)

    def test_disk_usage_is_consistent(self):
        result = disk_usage(".")
        self.assertGreater(result["total_bytes"], 0)
        self.assertGreaterEqual(result["free_bytes"], 0)
        self.assertLessEqual(result["used_percent"], 100)


class NetworkTests(unittest.TestCase):
    def test_subnet_description(self):
        result = describe_subnet("192.168.10.0/24")
        self.assertEqual(result["network"], "192.168.10.0")
        self.assertEqual(result["broadcast"], "192.168.10.255")
        self.assertEqual(result["usable_host_count"], 254)

    def test_subnet_accepts_host_bits(self):
        self.assertEqual(describe_subnet("10.0.0.7/24")["network"], "10.0.0.0")


if __name__ == "__main__":
    unittest.main()
