
from typing import Union, Any
import flask, typing
from types import SimpleNamespace
from collections import namedtuple


def get_query_string_values(expected: Union[str,list,None] = None, default: Any = None):
    """
    Returns the web request's args/values from the query string
    (after the "?" in the URL) as a SimpleNamespace.
    For easier use (args.x instead of args["x"]) and
    can ensure expected args are set (with default value)
    even if they are missing from the web request.

    :param expected: list of expected arg names as
        either a list or a string (comma-separated).
    :param default: value to assign to ALL missing args
    :return: the request args (as a SimpleNamespace)
    """
    a_dict = flask.request.args.to_dict()
    return _add_expected(a_dict, expected, default)


def get_form_values(expected: Union[str,list,None] = None, default: Any = None):
    """
    Returns the web request's args/values from the form
    (the body of a POST request) as a SimpleNamespace.
    For easier use (args.x instead of args["x"]) and
    can ensure expected args are set (with default value)
    even if they are missing from the web request.

    :param expected: list of expected arg names as
        either an array or a space or comma-separated string.
    :param default: value to assign to ALL missing args
    :return: the request args (as a SimpleNamespace)
    """
    a_dict = flask.request.form.to_dict()
    return _add_expected(a_dict, expected, default)


def _add_expected(a_dict, expected, default):
    args = SimpleNamespace(**a_dict)
    if expected:
        if isinstance(expected, str):
            if ',' in expected:
                expected = [a.strip() for a in expected.split(',')]
            else:
                expected = expected.split()
        for arg in expected:
            if not hasattr(args, arg):
                setattr(args, arg, default)
    return args
