import unittest
import json
import pyhydrate as pyhy


class DictReadMethods(unittest.TestCase):

    _data = pyhy.PyHydrate(json.loads(open('./pyhydrate/data/basic-list-get.json', 'r').read()), debug=True)

    def test_string_lookup(self):
        print('\n')
        self.assertEqual(' '.join(self._data[0]()), 'a set of strings')

    def test_integer_lookup(self):
        print('\n')
        self.assertEqual(sum(self._data[1]()), 6)

    def test_float_lookup(self):
        print('\n')
        self.assertEqual(self._data[2][3](), -10.9876)

    def test_bool_lookup(self):
        print('\n')
        self.assertEqual(self._data[3][1](), False)


if __name__ == '__main__':
    unittest.main()
