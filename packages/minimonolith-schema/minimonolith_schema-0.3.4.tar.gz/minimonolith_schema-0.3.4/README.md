# minimonolith-schema

`minimonolith-schema` is a Python package that provides functionality for validating the columns of data tables.

## Installation

Install the package via pip:

```
pip install minimonolith-schema
```

## Usage

Here's a simple example on how to use `minimonolith-schema`:

```python
import pandas_schema as pds
from minimonolith_schema import validators

schema = pds.Schema([
  pds.Column('Código Antiguo ', [pds.validation.CustomElementValidation(
    lambda x: validators.match_code_or_null(x,
      [r"^\d\d-\d\d\d$", r"^\d\d\d\d\d\d$"], ['No Aplica']), 'NOT_IN_PATTERNS')]),

  pds.Column('Código Vigente', [pds.validation.CustomElementValidation(
    lambda x: validators.in_int_interval(x, 100000, 300000), 'NOT_IN_PATTERNS')]),

  pds.Column('Nivel de Atención', [pds.validation.CustomElementValidation(
    lambda x: validators.in_category_or_null(x, ['Primario', 'Terciario', 'Secundario', 'terciario', 'Primario '],
    ['No Aplica', 'Pendiente']), 'NOT_IN_CATEGORY')]),
]);
```

# New Version
