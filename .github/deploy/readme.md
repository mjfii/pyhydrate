build the whl
```commandline
python -m build
```

install locally
```commandline
python -m installer pyhydrate-1.0.0-py3-none-any.whl
pip show pyhydrate
```

uninstall locally
```commandline
pip uninstall pyhydrate
```

check build
```commandline
twine check dist/*
```

upload to test
```commandline
twine upload -r testpypi dist/*
```

upload
```commandline
twine upload dist/*
```

load config of pypirc
```python
from twine import utils
print(utils.get_config('~/.pypirc'))
```