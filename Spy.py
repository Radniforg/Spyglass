from pprint import pprint
from urllib.parse import urlencode
import requests
import json
import time

def solitary_group(user1, maxpeople=0):
    #Получение id пользователя - удовлетворение условия "программа должна одинаково запускаться с ID и ника
    friend_count = 0
    response_id = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': TOKEN,
            'user_ids': user1,
            'v': 5.103
        }
    )
    #Получение списка друзей
    response_friends_list = requests.get(
        'https://api.vk.com/method/friends.get',
        params={
            'access_token': TOKEN,
            'user_id': response_id.json()['response'][0]['id'],
            'v': 5.103
        }
    )
    #получение ID друзей
    ids = str(response_friends_list.json()['response']['items'][0])
    for first_user_friend in response_friends_list.json()['response']['items'][1:]:
        ids = ids + ', ' + str(first_user_friend)
    print(ids)
    #Получение списка групп целевого пользователя и составление списка словарей групп
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
        time.sleep(1)
        print(f'{user_group["name"]}:')
        response_mutual_groups = requests.get(
            'https://api.vk.com/method/groups.isMember',
            params={
                'access_token': TOKEN,
                'group_id': user_group['id'],
                'user_ids': ids,
                'extended': 1,
                # 'fields': 'name', не работает! Не забыть спросить, почему!
                'v': 5.103
            }
        )
        friend_member = 0
        try:
            for user_membership in response_mutual_groups.json()['response']:
                if user_membership['member'] == 1:
                    friend_member += 1
            if friend_member <= maxpeople:
                user_group_list.append({'id': user_group['id'], 'name': user_group['name']})
        except KeyError:
            print('Error!\n\n\n')
            pprint(response_mutual_groups.json())
            print('\n\n\n')
        # pprint(response_mutual_groups.json())


    return user_group_list




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

TOKEN = '3714ec7679ee8e9352879d9f3a83f26ab7839cac1ed2421e2df7b99c4393c229b55b5e2758bd2c1d8b8c0'
user1_id = 4243253
user2_id = 6293784

pprint(solitary_group(6293784))