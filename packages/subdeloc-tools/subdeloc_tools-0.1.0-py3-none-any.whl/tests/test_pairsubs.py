import unittest
from subdeloc_tools.modules import pairsubs
from tests.constants.pairsubs import *

class TestSubTools(unittest.TestCase):
    def setUp(self):
        self.eng_file = "./tests/files/eng.ass"
        self.jap_file = "./tests/files/jap.ass"

    def test_pair_files(self):
        result = pairsubs.pair_files(self.eng_file, self.jap_file)
        self.assertEqual(result, RESULT)

if __name__ == "__main__":
    unittest.main()