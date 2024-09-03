# LiteAPI Python SDK

A Python SDK for interacting with the LiteAPI platform.

## Installation

```bash
pip install liteapi-sdk
```

## Usage

```python
from liteapi import LiteApi

api = LiteApi("your_api_key")
response = api.get_full_rates(data={...})
print(response)
```

## Testing

```
python -m unittest discover tests
```

---

## Build the package

```bash
pip install setuptools wheel
python3 setup.py sdist bdist_wheel
pip install twine
twine upload dist/*
```