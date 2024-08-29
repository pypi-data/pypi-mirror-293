# PyCEPSearch ![PyPI](https://img.shields.io/pypi/dm/PyCEPSearch)

This package helps you to get a CEP or Address from brazilian's postal service.

## Notes
Version 0.0.1:

- Get CEP by address
- Get address by CEP

## Installation

Use the package manager to install.

```bash
pip install PyCepSearch
```

## Usage

After install:
```python
from py_cep_search import cepsearch

search = cepsearch.CepSearch()
```
Get Addres by CEP
```python
address = search.get_address_by_cep("") #it returns a dict
```

Get CEP by Address
```python
cep = search.get_cep_by_address("") #it returns a list
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)