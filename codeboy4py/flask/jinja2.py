
import logging as log
import urllib

def jinja2_addons(flask_app):
    functions_to_add = (
        ('checked_if', _checked_if),
        ('selected_if', _selected_if),
    )
    filters_to_add = (
        ('urlencode', _urlencode),
        ('bnc_decimal', _bnc_decimal),
        ('bnc_csrf_tag', _bnc_csrf_tag),
        ('bnc_csrf_token', _bnc_csrf_token),
    )

    jinja_globals = flask_app.jinja_env.globals
    for function in functions_to_add:
        if function[0] not in jinja_globals:
            jinja_globals[function[0]] = function[1]
    jinja_filters = flask_app.jinja_env.filters
    for filter in filters_to_add:
        if filter[0] not in jinja_filters:
            jinja_filters[filter[0]] = filter[1]


# ----------------------------------------------------------------------
# Convenience functions for radio buttons and select lists
#   Example:    {{ checked_if(curr_value=='abc') }}
# ----------------------------------------------------------------------
def _checked_if(bool_value):
    return ' checked="1"' if bool_value else ''


def _selected_if(bool_value):
    return ' selected="1"' if bool_value else ''


# ----------------------------------------------------------------------
# GAE currently supports Jinja 2.6.  Add in missing useful filters:
# ----------------------------------------------------------------------
def _urlencode(value):          # similar to Jinja 2.7
    if isinstance(value, dict):
        return urllib.urlencode(value)
    return urllib.quote_plus(value.encode('utf-8'))


# ----------------------------------------------------------------------
# Convenience function for formatting decimal numbers
# ----------------------------------------------------------------------
def _bnc_decimal(value, ndigits=2, if_bad=None):
    """Alternative to Jinja2's "round", which doesn't format (no trailing zeros).
        Could use Jinja2's "format", but this does it all for you."""
    fmt='{:0,.' + str(ndigits) + 'f}'
    try:
        v = round(float(value), ndigits)
        v = fmt.format(v)
    except ValueError:
        v = if_bad if if_bad is not None else value
    return v



def _bnc_phone(value, fmt='(%)%-%', parts=(3,3,4), strip_leading=('1')):
    len = sum(parts)
    pass


from flask import session, request, abort
import uuid, hashlib
#-----------------------------------------------------------------------
# USAGE:
#  - In templates: <input name="_csrf_token" type="hidden" value="{{ ga_csrf_token() }}">
#  - In handler, at top or in app.before_request:  csrf_protect()
#
# See: http://flask.pocoo.org/snippets/3/
# @app.before_request
def csrf_abort_if_bad():
    if request.method in ['POST','PUT','PATCH','DELETE']:
        token = session.pop('_ga_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def csrf_is_okay(token_from_request=None, abort_code=None):
    token_from_session = session.pop('_ga_csrf_token', None)
    if not token_from_session  \
        or token_from_session != token_from_request:
        if abort_code is None:
            return False
        else:
            abort(abort_code)
    return True


def _bnc_csrf_tag():
    return '<input type="hidden" name="_csrf_token" value="%s">'  \
        .format(_bnc_csrf_token())

def _bnc_csrf_token():
    if '_ga_csrf_token' not in session:
        session['_csrf_token'] = str(uuid.uuid4())
    return session['_csrf_token']
