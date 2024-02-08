import unittest
import pyhydrate as pyhy


class PrimitiveReadMethods(unittest.TestCase):

    def test_string(self):
        print('\n')
        _data = pyhy.PyHydrate('a string', debug=True)
        self.assertEqual(_data(), 'a string')

    def test_int(self):
        print('\n')
        _data = pyhy.PyHydrate(123, debug=True)
        self.assertEqual(_data(), 123)

    def test_float(self):
        print('\n')
        _data = pyhy.PyHydrate(456.7890, debug=True)
        self.assertEqual(_data(), 456.7890)

    def test_bool(self):
        print('\n')
        _data = pyhy.PyHydrate(True, debug=True)
        self.assertEqual(_data(), True)

    def test_none(self):
        print('\n')
        _data = pyhy.PyHydrate(None, debug=True)
        self.assertEqual(_data(), None)

    def test_dict(self):
        print('\n')
        _data = pyhy.PyHydrate({}, debug=True)
        self.assertEqual(_data('yaml'), '{}')

    def test_list(self):
        print('\n')
        _data = pyhy.PyHydrate([], debug=True)
        self.assertEqual(_data('yaml'), '[]')
