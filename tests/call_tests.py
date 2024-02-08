import unittest
import json
import pyhydrate as pyhy


class CallMethods(unittest.TestCase):

    _data = pyhy.PyHydrate(json.loads(open('./pyhydrate/data/basic-dict-get.json', 'r').read()), debug=True)

    def test_yaml_string(self):
        print('\n')
        self.assertEqual(self._data.level_one.level_two.level_3.test_integer('yaml'), 'int: 1')

    def test_type(self):
        print('\n')
        self.assertEqual(self._data.level_one.level_two.level_3.test_integer('type'), int)

    def test_json_string(self):
        print('\n')
        self.assertEqual(self._data.level_one.level_two.level_3('json'),
                         '''{
   "test_string": "test string",
   "test_integer": 1,
   "test_float": 2.345,
   "test_bool": true
}''')


if __name__ == '__main__':
    unittest.main()
