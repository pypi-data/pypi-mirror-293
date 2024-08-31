import unittest
from subdeloc_tools.modules import honorific_fixer
from tests.constants.pairsubs import RESULT

class TestHonorificFixer(unittest.TestCase):
    def setUp(self):
        self.eng_file = "./tests/files/eng.ass"
        self.jap_file = "./tests/files/jap.ass"

    def test_prepare_edit_dict(self):
        result = honorific_fixer.prepare_edit_dict(RESULT)
        self.assertEqual(result, {'0': 'Hello', '1': 'Sir World'})

if __name__ == "__main__":
    unittest.main()