from pprint import pprint
from urllib.parse import urlencode
import requests
import json

APP_ID = 7423649
OAUTH_URL = 'https://oauth.vk.com/authorize'
OAUTH_PARAMS = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'groups,friends',
    'response_type': 'token',
    'v': 5.52
}
# print('?'.join((OAUTH_URL, urlencode(OAUTH_PARAMS))))

TOKEN = 'fd31b5b3e9480110ed2dfa8b974a60d5271810d6706a14f0b5964cbf2fe112c16d0ab02d632881c73be0f'
user1_id = 4243253
user2_id = 23289398
response_first = requests.get(
            'https://api.vk.com/method/groups.get',
            params={
                'access_token': TOKEN,
                # 'user_id': user1_id,
                'extended': 1,
                #'fields': 'name', не работает! Не забыть спросить, почему!
                'v': 5.103
            }
        )
# pprint(response_first.json())
response_second = requests.get(
            'https://api.vk.com/method/groups.get',
            params={
                'access_token': TOKEN,
                'user_id': user1_id,
                'extended': 1,
                'v': 5.103
            }
)
mutual_groups = []
# pprint(response_first.json()['response']['items'])
for group_first in response_first.json()['response']['items']:
    for group_second in response_second.json()['response']['items']:
        if group_first['id'] == group_second['id']:
            mutual_groups.append({'id': group_first['id'], 'name': group_first['name']})

pprint(mutual_groups)

# for group in mutual_groups:
#     response_group = requests.get(
#         'https://api.vk.com/method/groups.getAdresses',
#     )
