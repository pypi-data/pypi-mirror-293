import unittest
from subdeloc_tools.modules import pairsubs
from tests.constants.pairsubs import *

class TestPairSubs(unittest.TestCase):
    def setUp(self):
        self.eng_file = "./tests/files/eng.ass"
        self.jap_file = "./tests/files/jap.ass"

    def test_pair_files(self):
        result = pairsubs.pair_files(self.eng_file, self.jap_file)
        self.assertEqual(result, RESULT)

    def test_sanitize_string(self):
        result = pairsubs.sanitize_string("{\\pos(212,77)\\fscx50}Foo{\\fscx100}")
        self.assertEqual(result, "Foo")

if __name__ == "__main__":
    unittest.main()