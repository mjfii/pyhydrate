from pyhydrate import PyHydrate as PyHy

_doc = {
  "level-one": {
    "levelTWO": {
      "Level3": {
        "TestString": "test string",
        "testInteger": 1,
        "test_Float": 2.345,
        "Test_BOOL": True
      }
    }
  }
}

_demo = PyHy(_doc, debug=True)

print('\n', _demo.level_one.level_two, '\n')

print('\n', _demo.level_one.level_two('element'))