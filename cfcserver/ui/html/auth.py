
import flask as _flask
import functools, time
from cfcserver.services import auth as s_auth
from codeboy4py.flask.idioms import get_query_string_values
from .utils import render_svelte

_auth_callback = 'office/si/cb'


def auth(*args, signed_in=True, required_roles=None, api=False):
    def the_real_decorator(func):
        @functools.wraps(func)
        def decorated_func(*args, **kwargs):
            if signed_in or required_roles:
                # ---- User must be signed-in (have an active session)
                if 'auth_id' not in _flask.session:
                    return _flask.abort(401) if api \
                        else _flask.redirect('/office/si/p')

                now_ts = int(time.time())
                elapsed_time = now_ts - int(_flask.session.get('auth_ts', 0))
                if elapsed_time > 2*60*60:
                    return _flask.abort(401) if api \
                        else _flask.redirect('/office/si/to?next=' + _flask.request.full_path)
                _flask.session['auth_ts'] = now_ts

            if required_roles:
                # ---- User must have all required roles
                pass    # to be implemented
            return func(*args, **kwargs)
        return decorated_func

    if len(args) == 0:
        # Was called with key word args. Return the decorator.
        return the_real_decorator
    else:
        # Was called without key word args. Return the decorated function.
        return the_real_decorator(args[0])


def signin(action):
    if action == 'cb':
        return signin_callback()
    elif action == 'so':
        _flask.session.clear()
        return signin_prompt(signout=True)
    elif action == 'to':
        _flask.session.clear()
        return signin_prompt(timeout=True)
    else:  # action == 'p'
        return signin_prompt()


def signin_prompt(signout=False, timeout=False):
    vm = get_query_string_values('error,next')
    vm.signout, vm.timeout = signout, timeout
    auth_callback = _flask.request.host_url + _auth_callback
    vm.auth_code_reqs = s_auth.auth_code_request(auth_callback)
    # TODO: save auth_req.state in session.
    return render_svelte('SignIn', vm)


def signin_callback():
    req_args = get_query_string_values('error,code,state')
    error = req_args.error if req_args.error is not None \
        else 'missing_code' if req_args.code is None \
        else 'missing_state' if req_args.state is None \
        else None
    if error:
        return _flask.redirect('/office/si/p?error=' + error)

    auth_callback = _flask.request.host_url + _auth_callback
    r = s_auth.auth_code_to_userinfo(auth_callback, req_args.code, req_args.state)
    if r.error:
        return _flask.redirect(f'/office/si/p?error={r.error}')

    auth_id = (r.email or '').lower()
    if not s_auth.is_authorized(auth_id):
        error = f'user "{auth_id}" is not authorized'
        return _flask.redirect(f'/office/si/p?error={error}')
    _flask.session['auth_id'] = auth_id
    _flask.session['auth_ts'] = int(time.time())

    next_url = _flask.session.pop('next', '/office')
    return _flask.redirect(next_url)
