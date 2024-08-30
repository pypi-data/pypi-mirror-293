from .currencies import Currency_Formatter

__version__ = "1.0.2"



#// ----> Function imports <---- \\
Currency_Formatter = Currency_Formatter()

str_to_float = Currency_Formatter.str_to_float
as_percentage = Currency_Formatter.as_percentage
unit_abbreviator = Currency_Formatter.unit_abbreviator
format_currency = Currency_Formatter.format_currency
detect_currency = Currency_Formatter.detect_currency
custom_format = Currency_Formatter.custom_format
unspecified_currency = Currency_Formatter.unspecified_currency

# Currencies imports for IDEs to be able to show the documentation

BRL = Currency_Formatter.BRL
USD = Currency_Formatter.USD
EUR = Currency_Formatter.EUR
RUB = Currency_Formatter.RUB
GBP = Currency_Formatter.GBP
JPY = Currency_Formatter.JPY
CAD = Currency_Formatter.CAD
INR = Currency_Formatter.INR
AUD = Currency_Formatter.AUD
CHF = Currency_Formatter.CHF
CNY = Currency_Formatter.CNY
NZD = Currency_Formatter.NZD
MXN = Currency_Formatter.MXN
SGD = Currency_Formatter.SGD
SEK = Currency_Formatter.SEK
NOK = Currency_Formatter.NOK
PLN = Currency_Formatter.PLN
TRY = Currency_Formatter.TRY
HKD = Currency_Formatter.HKD
ILS = Currency_Formatter.ILS
KRW = Currency_Formatter.KRW
RMB = Currency_Formatter.RMB
COP = Currency_Formatter.COP
ARS = Currency_Formatter.ARS
AED = Currency_Formatter.AED
ZAR = Currency_Formatter.ZAR
THB = Currency_Formatter.THB
SAR = Currency_Formatter.SAR
DZD = Currency_Formatter.DZD
XPF = Currency_Formatter.XPF
XAF = Currency_Formatter.XAF
XOF = Currency_Formatter.XOF
XCD = Currency_Formatter.XCD