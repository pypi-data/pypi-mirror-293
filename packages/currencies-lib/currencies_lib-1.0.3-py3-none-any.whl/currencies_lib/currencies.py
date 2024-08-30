from functools import wraps

class Currency_Formatter():
    """This module handles values and formats them accordingly.

    ---

    #### General formatters:
    - `str_to_float(value)`: Converts a string value to a float.
    - `as_percentage(value, percentage)`: Formats a value as or with a percentage.
    - `unit_abbreviator(value)`: Abbreviates a value with a unit. (ex.: 1k)
    - `format_currency(value, **kwargs)`: Formats a value with a custom currency.
    - `detect_currency(value)`: Detects the currency from a string.
    - `unspecified_currency(value)`: Formats a value with an generic currency symbol ( ¤ )

    ---

    #### The currency formatter work as the following:
    - `Currency(value)`: Formats a value with a currency.
    - ex.: USD(1000) -> 1,000.00

    #### The module can handle the following currencies:
    - `BRL` | `USD` | `EUR` | `RUB` | `GBP` | `JPY` | `CAD` | `INR` | `AUD` 
    | `CHF` | `CNY` | `NZD` | `MXN` | `SGD` | `SEK` | `NOK` | `PLN` | `TRY` 
    | `HKD` | `ILS` | `KRW` | `RMB` | `COP` | `ARS` | `AED` | `ZAR` | `THB` 
    | `SAR` | `DZD` | `XPF` | `XAF` | `XOF` | `XCD` | `...`

    ---

    Example usage:
    ```python
    from currencies_lib import Currency_Formatter, USD

    value = 1000.50
    _ = Currency_Formatter.USD(value, currency_symbol=True)# Output: $ 1,000.50
    # Or
    _ = USD(value, currency_symbol=True)# Output: $ 1,000.50
    ```
    """

    def __init__(self):
        self._symbols = r" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz$£¢<>?!%&*(){}[]-=+~^|/"
        self._unit_abbreviator_dict = {1_000: 'k', 1_000_000: 'M', 1_000_000_000: 'B', 1_000_000_000_000: 'T'}
        self._right_positions = ["right", "r"]
        self._left_positions = ["left", "l"]
        self._currency_ban_symbols = r"ABCDEFGHIJKLMNOPQRSTUVWXYZ€₽£¥"
        self._currencies = {
            '$': 'USD',     'USD':'USD',
            'R$': 'BRL',    'BRL':'BRL',
            '€': 'EUR',     'EUR':'EUR',
            '₽': 'RUB',     'RUB':'RUB',
            '£': 'GBP',     'GBP':'GBP',
            '¥': 'JPY',     'JPY':'JPY',
            'C$': 'CAD',    'CAD':'CAD',
            '₹': 'INR',     'INR':'INR'
        }

    def _value_check(func):
        """Checks if the method has a valid value"""
        @wraps(func)
        def inner(self, value = None, *args, **kwargs):
            try:
                if not value:
                    print('\033[91m' + f'ERROR: Missing value for "Currency Formatter.{func.__name__}()"', '\033[0m')
                    return None
                if type(value) in (float, int):
                    pass
                else:
                    raise ValueError
            except ValueError:
                print(f'Currency Formatter: The inputted value is not a Integer or a Float. ("{type(value)}")')
                return None
            
            try:
                function_exec = func(self, value, **kwargs)
                return function_exec
            except Exception as e:
                print(e)
            return
        return inner

    @_value_check
    def as_percentage(self, value = None, percent = None, *, decimals=2, isfloat=True, subtraction=False) -> float:
        """Converts or adjusts a numeric value based on a given percentage.
        
        Can return a percentage of the value (e.g., 25% of 100 = 25) or reduce the value by the specified percentage (e.g., 100 reduced by 25% = 75)

        Parameters
        ----------
        value: int or float
            The value to be formatted
        percent: int or float (or str in cases like "20%")
            The percentage used to format the value

        - Optional Kwargs
        
        subtraction: bool
            Defines if the value should be subtracted by the percenatege or not, by default False
        decimals: int
            Defines the decimal places in the final value, by default 2
        isfloat: bool
            Forces the value as a float number, by default True
        """
        try:
            if not percent:
                print('Currency Formatter: The percentage value is missing.')
                return None
            if isinstance(percent, str):
                percent = float(percent.replace("%", ""))
            match subtraction:
                case True:
                    final_value = f"{value - (percent * float(value) / 100):.{decimals}f}"
                case False:
                    final_value = f"{percent * float(value) / 100:.{decimals}f}"

            if isfloat == True:
                return float(final_value)
            return final_value
        
        except Exception as e:
            print(e)
        
        return None

    @_value_check
    def custom_format(self, value = None, *, currency_symbol: str=None,
            sign_position: str='LEFT',
            thousands_sep: str=',', decimal_sep: str='.',
            custom_format=None) -> str:
        """The use of this method is not recommended. Only use it if you know what you're doing.

        Instead, use "format_currency" to a custom format.

        This method is used to input custom formats such as f"{:.2f}"
        """
        if not custom_format:
            print(f'Currency Formatter: Format must be provided.')
            return None
        if type(custom_format) != str:
            print(f'Currency Formatter: The inputted format is not a String type. ("{type(custom_format)}")')
            return None
        if len(custom_format) < 1:
            print(f'Currency Formatter: The inputted format is empty. ("{custom_format}")')
            return None
        if decimal_sep == custom_format[:1]:
            print(f'Currency Formatter: The decimal_sep cannot be the same as the custom_format. ("{decimal_sep}")')
            return None
        
        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            match sign_position:
                case "RIGHT":
                    final_value = f"{float(value):{custom_format}}{(" " + currency_symbol) if currency_symbol != None else ""}"
                    final_value = final_value.replace('.', decimal_sep).replace(f'{custom_format[:1]}', thousands_sep)
                case "LEFT":
                    final_value = f"{(currency_symbol + " ") if currency_symbol != None else ""}{float(value):{custom_format}}"
                    final_value = final_value.replace('.', decimal_sep).replace(f'{custom_format[:1]}', thousands_sep)
            
            return final_value
        
        except ValueError:
            print(f'Currency Formatter: Invalid format inputted. ("{custom_format[0]}")')

        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(f'Currency Formatter (Unexpected): {e}')

        return None
   
    @_value_check
    def unit_abbreviator(self, value = None, decimals=1) -> str:
        # 1000 as > 1k || 1000000 as > 1M
        """Abbreviates a numeric value to its corresponding unit acronym (e.g., 1000 -> 1k).

        Parameters
        ----------
        value : int or float
            numeric value to abbreviate
        decimals : int, optional
            number of decimal places, by default 1

        Returns
        -------
        str
            abbreviated value
            -->> 1k, 1M, 1B, etc.
        """
        
        try:
            for divisor, suffix in sorted(self._unit_abbreviator_dict.items(), reverse=True):
                if abs(value) >= divisor:
                    abbreviated_value = value / divisor
                    return f"{abbreviated_value:.{decimals}f}{suffix}"
            return f'{value:.2f}'
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def format_currency(self, value: float = None, *, currency_symbol:str ='',
            sign_position:str ='left', thousands_sep:str =',',
            decimal_sep: str ='.', decimals: int = 2) -> str:
        """Formats a value to a specified currency format
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `currency_symbol` (str): Defines the currency symbol, by default None ('')
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """
        
        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol:
                if sign_position in self._right_positions:
                    sign_position = "RIGHT"
                elif sign_position in self._left_positions:
                    sign_position = "LEFT"
                else:
                    raise ReferenceError
                match sign_position:
                    case 'LEFT':
                        final_value = f"{currency_symbol}{final_value}"
                    case 'RIGHT':
                        final_value = f"{final_value}{currency_symbol}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None

    def detect_currency(self, value:str = None) -> str:
        """Detects the currency used in a string
        
        Available currencies for detection:
        USD | BRL | EUR | RUB | GBP | JPY | CAD | INR

        Parameters
        ----------
        value : str
            Value to be analized

        Returns
        -------
        str
            Returns the currency if detected
        """
        try:
            if not value:
                raise ValueError("Currency Formatter: The value must be provided")
            for symbol, currency in self._currencies.items():
                if symbol in value and not value[(value.rfind(symbol)-1)] in self._currency_ban_symbols:
                    return currency
            raise RuntimeError

        except RuntimeError:
            print(f'Currency Formatter: Unable to detect the currency of "{value}"')

        except Exception as e:
            print(e)
        
        return None

    def str_to_float(self, value:str = None) -> float:
        """Translates a string formatted value to float
        (e.g. "$ 1.000,50" to 1000.50)

        Parameters
        ----------
        value : str
            String value to be formatted
        """
        # Can be imprecise
        try:
            if not value:
                raise ValueError("Currency Formatter: The value must be provided")
            __number_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            for i, __none in enumerate(value):
                if value[i] in __number_list:
                    negative_num = False
                    break

                if value[i] == '-':
                    negative_num = True
                    break

            if any(char in value for char in self._symbols):
                for char in self._symbols:
                    value = value.replace(char, '')

            if ',' in value and '.' in value:
                if value.rfind(',') > value.rfind('.'):
                    value = value.replace('.', '')
                    value = value.replace(',', '.')
                else:
                    value = value.replace(',', '')

            elif ',' in value:
                value = value.replace(',', '.')
            
            elif '.' in value:
                value = value.replace('.', '')
            
            if negative_num:
                final_value = float('-' + value)
                return final_value
                    
            final_value = float(value)
            return final_value

        except ValueError:
            print(f"Currency Formatter: Unable to convert '{value}' to float")
                    
        except Exception as e:
            print("Currency Formatter:", e)
        
        return None

    @_value_check
    def unspecified_currency(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',',currency_symbol=True,
            sign_position="LEFT", decimals=2) -> str:
        """Formats a value to a non specified currency format with the "¤" symbol.
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `currency_symbol` (str): Defines if the symbol should be used, by default True
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            if currency_symbol == True:
                match sign_position:
                    case "RIGHT":
                        final_value = f"{float(value):_.{decimals}f} ¤".replace('.', decimal_sep).replace('_', thousands_sep)
                    case "LEFT":
                        final_value = f"¤ {float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            else:
                final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None

    @_value_check
    def BRL(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Brazilian Real (BRL)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"R$ {final_value}"             

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def USD(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to United States Dollar (USD)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"$ {final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def EUR(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',', sign_position="LEFT",
            currency_symbol=False, eur_sign=False, decimals=2) -> str:
        """Formats a value to Euro (EUR)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `eur_sign` (bool): Defines if the € sign is shown, by default False 
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            if currency_symbol == True:
                if eur_sign == True:
                    eur_sign = "€"
                elif eur_sign == False:
                    eur_sign = "EUR"

                match sign_position:
                    case "RIGHT":
                        final_value = f"{float(value):_.{decimals}f} {eur_sign}".replace('.', decimal_sep).replace('_', thousands_sep)
                    case "LEFT":
                        final_value = f"{eur_sign} {float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            else:
                final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def RUB(self, value = None, *, thousands_sep: str = ' ',
            decimal_sep: str = ',',
            currency_symbol=False, sign_position="LEFT", decimals=2) -> str:
        """Formats a value to Russian Ruble (RUB)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ' '
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            if currency_symbol == True:
                match sign_position:
                    case "RIGHT":
                        final_value = f"{float(value):_.{decimals}f} ₽".replace('.', decimal_sep).replace('_', thousands_sep)
                    case "LEFT":
                        final_value = f"₽ {float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            else:
                final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def GBP(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to British Pound (GBP)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"£{final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def JPY(self, value = None, *, thousands_sep: str = ',',
            currency_symbol=False) -> str:
        """Formats a value to Japanese Yen (JPY)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        """

        try:
            final_value = f"{float(value):_.0f}".replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"¥{final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def CAD(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.', spaced_sign=True,
            currency_symbol=False, cad_sign=True, decimals=2) -> str:
        """Formats a value to Canadian Dollar (CAD)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency symbol is shown, by default False
        -    `cad_sign` (bool): Defines if the C$ sign is shown, by default False
        -    `spaced_sign` (bool): Defines if the sign will have a space after it, by default True
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                match cad_sign:
                    case True:
                        cad_sign = "C$"
                    case False:
                        cad_sign = "$"
                if spaced_sign == True:
                    cad_sign += " "

                final_value = f"{cad_sign}{final_value}"
                
            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def INR(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Indian Rupee (INR)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            if value >= 100000 or value <= -100000:
                if str(value).startswith('-'):
                    negative_num = True
                    value = str(value)[1:]
                else:
                    negative_num = False
                if '.' in str(value):
                    int_value, dec_value = f'{float(value):.2f}'.split('.')
                else:
                    int_value = f'{value}'
                    dec_value = None
                if len(int_value) > 3:
                    int_value = int_value[::-1]
                    int_value = [int_value[:3]] + [int_value[i:i + 2] for i in range(3, len(int_value), 2)]
                    int_value = thousands_sep.join(int_value)[::-1]

                final_value = (
                    ('-' if negative_num else '') + int_value +
                    (decimal_sep + dec_value if dec_value else decimal_sep +('0' * decimals))
                )
                if currency_symbol:
                    final_value = f'₹{final_value}'
                    
                return final_value

            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol:
                final_value = f'₹{final_value}'

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def AUD(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Australian Dollar (AUD)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"A$ {final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def CHF(self, value = None, *, thousands_sep: str = "'",
            decimal_sep: str = '.',
            currency_symbol=False, currency_sign=True, decimals=2) -> str:
        """Formats a value to Swiss Franc (CHF)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default "'"
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `currency_sign` (bool): Defines if the ₣ sign is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                match currency_sign:
                    case True:
                        currency_sign = "CHF"
                    case False:
                        currency_sign = "₣"

                final_value = f"{currency_sign} {final_value}"
                
            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def CNY(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Chinese Yuan (CNY)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"¥{final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def NZD(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to New Zealand Dollar (NZD)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"NZ$ {final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def MXN(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.', sign_position="LEFT",
            currency_symbol=False, mxn_sign=False, decimals=2) -> str:
        """Formats a value to Mexican Peso (MXN)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `mxn_sign` (bool): Defines if the MX$ sign is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            if currency_symbol == True:
                if mxn_sign == True:
                    mxn_sign = "MX$"
                elif mxn_sign == False:
                    mxn_sign = "$"

                match sign_position:
                    case "RIGHT":
                        final_value = f"{float(value):_.{decimals}f} {mxn_sign}".replace('.', decimal_sep).replace('_', thousands_sep)
                    case "LEFT":
                        final_value = f"{mxn_sign} {float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            else:
                final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None

    @_value_check
    def SGD(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Singapore Dollar (SGD)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"S$ {final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def SEK(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Swedish Krona (SEK)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"{final_value} kr"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def NOK(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Norwegian Krona (NOK)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"{final_value} kr"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def DKK(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Danish Krona (DKK)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"{final_value} kr"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def PLN(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Polish Zloty (PLN)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"{final_value} zł"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def TRY(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Turkish Lira (TRY)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"₺{final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def HKD(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Hong Kong Dollar (HKD)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"HK$ {final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def ILS(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Israeli New Shekel (ILS)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"₪ {final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def KRW(self, value = None, *, thousands_sep: str = ',',
            currency_symbol=False) -> str:
        """Formats a value to South Korean Won (KRW)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        """

        try:
            final_value = f"{float(value):_.0f}".replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"₩{final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def RMB(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, decimals=2) -> str:
        """Formats a value to Chinese Yuan (RMB)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"¥{final_value}"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def COP(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',', sign_position="LEFT",
            currency_symbol=False, cop_sign=False, decimals=2) -> str:
        """Formats a value to Colombian Peso (COP)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `cop_sign` (bool): Defines if the 'COP' sign is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            if currency_symbol == True:
                if cop_sign == True:
                    cop_sign = "COP"
                elif cop_sign == False:
                    cop_sign = "$"

                match sign_position:
                    case "RIGHT":
                        final_value = f"{float(value):_.{decimals}f} {cop_sign}".replace('.', decimal_sep).replace('_', thousands_sep)
                    case "LEFT":
                        final_value = f"{cop_sign} {float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            else:
                final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None

    @_value_check
    def ARS(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',', sign_position="LEFT",
            currency_symbol=False, ars_sign=False, decimals=2) -> str:
        """Formats a value to Argentine Peso (ARS)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `ars_sign` (bool): Defines if the AR$ sign is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            if currency_symbol == True:
                if ars_sign == True:
                    ars_sign = "AR$"
                elif ars_sign == False:
                    ars_sign = "$"

                match sign_position:
                    case "RIGHT":
                        final_value = f"{float(value):_.{decimals}f} {ars_sign}".replace('.', decimal_sep).replace('_', thousands_sep)
                    case "LEFT":
                        final_value = f"{ars_sign} {float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            else:
                final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None

    def AED(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',', sign_position="LEFT",
            currency_symbol=False, aed_sign=False, decimals=2) -> str:
        """Formats a value to United Arab Emirates Dirham (AED)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `aed_sign` (bool): Defines if the "د.إ" sign is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            if currency_symbol == True:
                if aed_sign == True:
                    aed_sign = "د.إ"
                elif aed_sign == False:
                    aed_sign = "AED"

                match sign_position:
                    case "RIGHT":
                        final_value = f"{float(value):_.{decimals}f} {aed_sign}".replace('.', decimal_sep).replace('_', thousands_sep)
                    case "LEFT":
                        final_value = f"{aed_sign} {float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            else:
                final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None

    def ZAR(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, zar_sign=False, decimals=2) -> str:
        """Formats a value to South African Rand (ZAR)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `zar_sign` (bool): Defines if the R sign is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                match zar_sign:
                    case True:
                        zar_sign = "R"
                    case False:
                        zar_sign = "ZAR"

                final_value = f"{zar_sign}{final_value}"
                
            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    def THB(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.',
            currency_symbol=False, thb_sign=False, decimals=2) -> str:
        """Formats a value to Thai Baht (THB)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `thb_sign` (bool): Defines if the ฿ sign is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                match thb_sign:
                    case True:
                        thb_sign = "฿"
                    case False:
                        thb_sign = "THB"

                final_value = f"{thb_sign}{final_value}"
                
            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None

    def SAR(self, value = None, *, thousands_sep: str = '.',
            decimal_sep: str = ',', sign_position="LEFT",
            currency_symbol=False, sar_sign=False, decimals=2) -> str:
        """Formats a value to Saudi Riyal (SAR)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `decimal_sep` (str): Separator for decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `CUR_sign` (bool): Defines if the "ر.س" sign is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            if currency_symbol == True:
                if sar_sign == True:
                    sar_sign = "ر.س"
                elif sar_sign == False:
                    sar_sign = "SAR"

                match sign_position:
                    case "RIGHT":
                        final_value = f"{float(value):_.{decimals}f} {sar_sign}".replace('.', decimal_sep).replace('_', thousands_sep)
                    case "LEFT":
                        final_value = f"{sar_sign} {float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            else:
                final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None

    # Dois padrões de moeda e 1 posição
    @_value_check
    def XCD(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.', currency_symbol=False,
            xcd_sign=False, decimals=2) -> str:
        """Formats a value to East Caribbean Dollar (XCD)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `xcd_sign` (bool): Defines if the EC$ sign is shown, by default False
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                match xcd_sign:
                    case True:
                        xcd_sign = "EC$"
                    case False:
                        xcd_sign = "$"

                final_value = f"{xcd_sign}{final_value}"
                
            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def XOF(self, value = None, *, thousands_sep: str = ',',
            currency_symbol=False) -> str:
        """Formats a value to West African CFA Franc (XOF)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        """

        try:
            final_value = f"{float(value):_.0f}".replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"{final_value} CFA"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep}")')
        
        except Exception as e:
            print(e)

        return None

    @_value_check
    def XAF(self, value = None, *, thousands_sep: str = ',',
            currency_symbol=False) -> str:
        """Formats a value to CURRENCY
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        """

        try:
            final_value = f"{float(value):_.0f}".replace('_', thousands_sep)
            if currency_symbol == True:
                final_value = f"{final_value} FCFA"

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep}")')
        
        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def XPF(self, value = None, *, thousands_sep: str = ',',
            currency_symbol=False, sign_position="LEFT") -> str:
        """Formats a value to CURRENCY
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        """

        try:
            sign_position = sign_position.lower()
            if sign_position not in self._right_positions and sign_position not in self._left_positions:
                print(f'Currency Formatter: Invalid sign_position inputted. ("{sign_position}")')
                return None
            
            if sign_position in self._right_positions:
                sign_position = "RIGHT"
            elif sign_position in self._left_positions:
                sign_position = "LEFT"
            else:
                raise ReferenceError

            if currency_symbol == True:
                match sign_position:
                    case "RIGHT":
                        final_value = f"{float(value):_.0f} F".replace('_', thousands_sep)
                    case "LEFT":
                        final_value = f"₣{float(value):_.0f}".replace('_', thousands_sep)
            else:
                final_value = f"{float(value):_.0f}".replace('_', thousands_sep)

            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep}")')
        
        except ReferenceError:
            print(f'Currency Formatter: The inputted position is not valid. Must be left or right. ("{sign_position}")')

        except Exception as e:
            print(e)

        return None
    
    @_value_check
    def DZD(self, value = None, *, thousands_sep: str = ',',
            decimal_sep: str = '.', spaced_sign=True,
            currency_symbol=False, dzd_sign=True, decimals=2) -> str:
        """Formats a value to Algerian Dinar (DZD)
        ### Args:
        -    `value` (int or float): Value to be formatted
        ---
        ### Optional kwargs:
        -    `thousands_sep` (str): Separator for thousand decimal places, by default ','
        -    `decimal_sep` (str): Separator for decimal places, by default '.'
        -    `currency_symbol` (bool): Defines if the currency_symbol is shown, by default False
        -    `sign_position` (str): Defines the position for the currency_symbol, by default "left"
        -    `dzd_sign` (bool): Defines if the "دج" sign is shown, by default False
        -    `spaced_sign` (bool): Defines if the sign will have a space after it, by default True
        -    `decimals` (int): Number of decimal places when formatted, by default 2
        """

        try:
            final_value = f"{float(value):_.{decimals}f}".replace('.', decimal_sep).replace('_', thousands_sep)
            if currency_symbol == True:
                match dzd_sign:
                    case True:
                        dzd_sign = "دج"
                    case False:
                        dzd_sign = "DA"
                if spaced_sign == True:
                    dzd_sign += " "

                final_value = f"{final_value} {dzd_sign}"
                
            return final_value
        
        except TypeError:
            print(f'Currency Formatter: The inputted value is not a String type. ("{thousands_sep if not isinstance(thousands_sep, str) else decimal_sep}")')
        
        except Exception as e:
            print(e)

        return None