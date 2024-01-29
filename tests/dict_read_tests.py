import unittest
import json
import pyhydrate as pyhy


class DictReadMethods(unittest.TestCase):

    _data = pyhy.PyHydrate(json.loads(open('./pyhydrate/data/basic-test-001.json', 'r').read()))

    def test_string_lookup(self):
        self.assertEqual(self._data.query_string_parameters.test_string(), 'test string')

    def test_integer_lookup(self):
        self.assertEqual(self._data.query_string_parameters.test_integer(), 1)

    def test_float_lookup(self):
        self.assertEqual(self._data.query_string_parameters.test_float(), 2.345)

    def test_bool_lookup(self):
        self.assertEqual(self._data.query_string_parameters.test_bool(), True)


if __name__ == '__main__':
    unittest.main()
