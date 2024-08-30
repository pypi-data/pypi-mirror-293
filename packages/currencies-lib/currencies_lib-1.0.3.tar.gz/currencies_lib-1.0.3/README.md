# Currencies Formatter

The **Currencies Formatter Library** (or currencies lib) is a Python library designed to simplify the formatting of monetary values for various currencies. It supports a wide range of currencies and provides options for custom formatting. Whether you need to display values with currency symbols or abbreviate large numbers, this library offers a straightforward solution.

### Features
- Format monetary values for a variety of currencies.
- Customizable formatting options for currency symbols and decimal places.
- Supports both standard and custom currency symbols.
- Allows conversion of values to percentage format.
- Utility functions for abbreviating units and detecting currency symbols.
>
### Installing
You can install this library with:
```bash
$ pip install currencies-lib
```
>

### Example of use

```python
from currencies_lib import BRL

value = 1250.50
result = BRL(value, currency_symbol=True)
print(result)
#> "R$ 1.250,50"
```
or
```python
from currencies_lib import *

value = 1250.50
result = Currency_Formatter.EUR(value, currency_symbol=True, eur_sign=True)
print(result)
#> "€ 1.250,50"
```
**Note**: Direct imports from the currencies_lib module are not recommended. Use from currencies_lib import ... to access specific formatters or all of them "*".

>

### Contributing

I welcome contributions to improve this library! If you have suggestions, bug reports, or new feature requests, please open an issue or submit a pull request on my [GitHub repository](https://github.com/iamtwobe/currencies_lib).
>

### License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/iamtwobe/currencies_lib/blob/main/LICENSE) file for details.