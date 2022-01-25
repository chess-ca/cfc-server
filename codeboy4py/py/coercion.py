
from typing import Union
import decimal, datetime

_undefined = object()   # since caller may want None as a value


class CoercionError(ValueError):
    pass


def str_to_int(aString: str, if_bad=_undefined) -> Union[int, CoercionError]:
    try:
        return int(aString)
    except ValueError as ve:
        return if_bad if if_bad is not _undefined \
            else CoercionError(f'999: "{aString}" is not an integer')


def str_to_float(aString: str, if_bad=_undefined) -> Union[float, CoercionError]:
    try:
        return float(aString)
    except ValueError as ve:
        return if_bad if if_bad is not _undefined \
            else CoercionError(f'999: "{aString}" is not a float')


def str_to_decimal(aString: str, if_bad=_undefined) -> Union[decimal.Decimal, CoercionError]:
    try:
        return decimal.Decimal(aString)
    except ValueError as ve:
        return if_bad if if_bad is not _undefined \
            else CoercionError(f'999: "{aString}" is not a decimal')


def iso_str_to_date(aString: str, if_bad=_undefined) -> Union[datetime.date, CoercionError]:
    """
    :param aString: in ISO date format: YYYY-MM-DD.
    """
    try:
        return datetime.date.fromisoformat(aString)
    except ValueError as ve:
        return if_bad if if_bad is not _undefined \
            else CoercionError(f'999: "{aString}" is not a date')


def iso_str_to_datetime(aString: str, if_bad=_undefined) -> Union[datetime.datetime, CoercionError]:
    """
    :param aString: in ISO date/time/time-zone format:
        YYYY-MM-DD[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]]
        where "*" matches any character.
    """
    try:
        return datetime.datetime.fromisoformat(aString)
    except ValueError as ve:
        return if_bad if if_bad is not _undefined \
            else CoercionError(f'999: "{aString}" is not a date/time')
