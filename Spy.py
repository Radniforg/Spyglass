##

APP_ID = 7423649
OAUTH_URL = 'https://oauth.vk.com/authorize'
OAUTH_PARAMS = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'status,friends',
    'response_type': 'token',
    'v': 5.52
}
print('?'.join((OAUTH_URL, urlencode(OAUTH_PARAMS))))

