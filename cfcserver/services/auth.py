
import urllib.parse, urllib.request, urllib.error
import secrets, types, json
from cfcserver.models.appconfig import AppConfig

_authorized_emails = AppConfig.AUTH_EMAILS.split()


def auth_code_request(callback_url: str) -> types.SimpleNamespace:
    ret = types.SimpleNamespace(error=None)
    state = secrets.token_urlsafe(8)
    # ---- Google
    scope = 'https://www.googleapis.com/auth/userinfo.email'
    ret.google_url = ''.join((
        'https://accounts.google.com/o/oauth2/auth',
        '?response_type=code',
        '&client_id=', AppConfig.AUTH_GOOGLE_CLIENT_ID,
        '&redirect_uri=', urllib.parse.quote(callback_url, safe=''),
        '&scope=', urllib.parse.quote(scope, safe=''),
        '&state=', f'g-{state}'
    ))
    return ret


def auth_code_to_userinfo(callback_url: str, code: str, state: str) -> types.SimpleNamespace:
    if state.startswith('g-'):
        return _get_userinfo_from_google(callback_url, code)
    raise NotImplementedError(f'Unexpected state="{state[:6]}..." does not indicate Auth Provider')


def _get_userinfo_from_google(callback_url, code):
    ret = types.SimpleNamespace(error=None)
    # -------- Step 1: Get access token by providing the code & secret
    request_data=urllib.parse.urlencode(dict(
        grant_type='authorization_code',
        code=code,
        client_id=AppConfig.AUTH_GOOGLE_CLIENT_ID,
        client_secret=AppConfig.AUTH_GOOGLE_CLIENT_SECRET,
        redirect_uri=callback_url,
        scope='',   # (not needed)
    ))
    request = urllib.request.Request(
        method='POST',
        url='https://oauth2.googleapis.com/token',
        data=request_data.encode('ascii'),
    )
    try:
        with urllib.request.urlopen(request) as rsp:
            token = json.load(rsp)
    except urllib.error.HTTPError as e:
        ret.error = f'HTTPError (get token): {e.code}: {e.reason}'
        return ret
    # token.keys(): access_token, id_token?, expires_in, token_type, scope, refresh_token

    # -------- Step 2: Call the Userinfo API providing the access token
    request = urllib.request.Request(
        method='GET',
        url='https://www.googleapis.com/oauth2/v2/userinfo',
        headers={
            'Authorization': f'Bearer {token["access_token"]}'
        },
    )
    try:
        with urllib.request.urlopen(request) as rsp:
            userinfo = json.load(rsp)
    except urllib.error.HTTPError as e:
        ret.error = f'HTTPError (get userinfo): {e.code}: {e.reason}'
        return ret

    ret.email = userinfo['email']
    ret.email_verified = userinfo['verified_email']
    ret.id = userinfo['id']
    return ret


def is_authorized(email):
    return email in _authorized_emails
