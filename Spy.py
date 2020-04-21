from pprint import pprint
from urllib.parse import urlencode
import requests
import json

def solitary_group(user1):
    response_id = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': TOKEN,
            'user_ids': user1,
            'v': 5.103
        }
    )
    response_friends_list = requests.get(
        'https://api.vk.com/method/friends.get',
        params={
            'access_token': TOKEN,
            'user_id': response_id.json()['response'][0]['id'],
            'v': 5.103
        }
    )
    response_user_groups = requests.get(
        'https://api.vk.com/method/groups.get',
        params={
            'access_token': TOKEN,
            'user_id': user1,
            'extended': 1,
            # 'fields': 'name', не работает! Не забыть спросить, почему!
            'v': 5.103
        }
    )
    user_group_list = []
    for user_group in response_user_groups.json()['response']['items']:
        user_group_list.append({'id': user_group['id'], 'name': user_group['name']})
    for friend in response_friends_list.json()['response']['items']:
        response_friend_groups = requests.get(
            'https://api.vk.com/method/groups.get',
            params={
                'access_token': TOKEN,
                'user_id': friend,
                'extended': 1,
                # 'fields': 'name', не работает! Не забыть спросить, почему!
                'v': 5.103
            }
        )
        print(f'Id - {friend};', end='')
        try:
            print(f' first group - {response_friend_groups.json()["response"]["items"][0]}')
        except KeyError:
            print('')
        except IndexError:
            print('')
    return user_group_list


    response_second = requests.get(
        'https://api.vk.com/method/groups.get',
        params={
            'access_token': TOKEN,
            'user_id': user2,
            'extended': 1,
            'v': 5.103
        }
    )
    solitary_groups = []
    for group_first in response_first.json()['response']['items']:
        solitary = 1
        for group_second in response_second.json()['response']['items']:
            if group_first['id'] == group_second['id']:
                solitary = 0
        if solitary == 1:
            solitary_groups.append({'id': group_first['id'], 'name': group_first['name']})

    # pprint(solitary_groups)
    # print(f'count: {len(solitary_groups)}')
    return None


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
user2_id = 6293784

pprint(solitary_group(6293784))