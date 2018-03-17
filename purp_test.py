import unittest


# Returns list of files for testcases for given typ and verb
def set_up_basic_cases(typ, verb):
    filelist = []
    for direct_obj in ["boo", "flt", "non_exist", "str", "int"]:
        filelist.append("test/{}_{}_{}.txt".format(typ, verb, direct_obj))
    return filelist


class TestPurp(unittest.TestCase):

    def test_int_hold(self):
        filelist = set_up_basic_cases("int", "hold")
        for file in filelist:
            self.assertEqual(0, 0)

    def test_str_hold(self):
        filelist = set_up_basic_cases("str", "hold")
        for file in filelist:
            self.assertEqual(0, 0)

    def test_flt_hold(self):
        filelist = set_up_basic_cases("flt", "hold")
        for file in filelist:
            self.assertEqual(0, 0)

    def test_boo_hold(self):
        filelist = set_up_basic_cases("boo", "hold")
        for file in filelist:
            self.assertEqual(0, 0)


if __name__ == '__main__':
    unittest.main()