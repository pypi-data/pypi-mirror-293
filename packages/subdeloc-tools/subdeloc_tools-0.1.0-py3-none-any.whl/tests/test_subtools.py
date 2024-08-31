import unittest
from subdeloc_tools import subtools as st
from tests.constants.subtools import *

class TestSubTools(unittest.TestCase):

    def test_init(self):
        ST = st.SubTools("./tests/files/eng.ass", "./tests/files/jap.ass", "./tests/files/names.json", "./subdeloc_tools/honorifics.json")
        self.assertEqual(ST.main_sub, "./tests/files/eng.ass")
        self.assertEqual(ST.ref_sub, "./tests/files/jap.ass")
        self.assertEqual(ST.honorifics["honorifics"]["san"]["kanjis"][0], "さん")
        self.assertEqual(ST.names["Hello"], "こんにちは")

    def test_honor_array(self):
        ST = st.SubTools("./tests/files/eng.ass", "./tests/files/jap.ass", "./tests/files/names.json", "./subdeloc_tools/honorifics.json")
        self.assertEqual(ST.prepare_honor_array(), HONORIFICS_ARRAY)

if __name__ == "__main__":
    unittest.main()