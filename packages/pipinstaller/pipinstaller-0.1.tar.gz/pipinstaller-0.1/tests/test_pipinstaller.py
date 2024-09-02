# tests/test_installer.py

import unittest
from pipinstaller.pipinstaller import search_package

class TestInstaller(unittest.TestCase):
    def test_search_package(self):
        # Example test case
        self.assertTrue(search_package("requests"))

if __name__ == "__main__":
    unittest.main()
