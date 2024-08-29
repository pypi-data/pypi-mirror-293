# PyRegBL

Python package to get RegBL information easily.

## Get started

Install the package with pip

```bash
pip install PyRegBL
```

## Usage

The package is small. Here are the main functions you can use:

```python
import pyregbl

# Get a RegBL entry
pyregbl.get('9032962', raw=False)

# Get attributes of a RegBL entry with their descriptions 
pyregbl.get_attributes()

# Get the mapping table allowing to convert RegBL attributes values to their descriptions
pyregbl.get_mapping_table()

# Map a raw RegBL entry to a human-readable one (with descriptions)
raw = pyregbl.get('9032962', raw=True)
pyregbl.map(raw['feature']['attributes'])
```

## Miscellaneous

- RegBL character catalog : https://www.housing-stat.ch/files/882-2200.pdf

## Contact

Fred Montet (fredmontet@gmail.com)
