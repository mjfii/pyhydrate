import unittest
import json
import pyhydrate as pyhy


class DictReadMethods(unittest.TestCase):

    _data = pyhy.PyHydrate(json.loads(open('./pyhydrate/data/basic-dict-get.json', 'r').read()), debug=True)

    def test_string_lookup(self):
        print('\n')
        self.assertEqual(self._data.level_one.level_two.level_3.test_string(), 'test string')

    def test_integer_lookup(self):
        print('\n')
        self.assertEqual(self._data.level_one.level_two.level_3.test_integer(), 1)

    def test_float_lookup(self):
        print('\n')
        self.assertEqual(self._data.level_one.level_two.level_3.test_float(), 2.345)

    def test_bool_lookup(self):
        print('\n')
        self.assertEqual(self._data.level_one.level_two.level_3.test_bool(), True)


if __name__ == '__main__':
    unittest.main()
