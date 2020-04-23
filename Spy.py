from pprint import pprint
from urllib.parse import urlencode
import requests
import json
import time

def solitary_group(user1, maxpeople=0):
    #Получение id пользователя - удовлетворение условия "программа должна одинаково запускаться с ID и ника
    username_confirmation = False
    while not username_confirmation:
        response_id = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'access_token': TOKEN,
                'user_ids': user1,
                'v': 5.103
            }
        )
        try:
            user_id = response_id.json()['response'][0]['id']
            username_confirmation = True
        except KeyError:
            correct_input = False
            while not correct_input:
                function_suspension = input('Некорректное имя пользователя. Хотите продолжить (Y/N):\n')
                if function_suspension.lower() == 'n':
                    return 'Программа остановлена пользователем. Некорректное имя пользователя'
                elif function_suspension.lower() == 'y':
                    user1 = input('Пожалуйста, введите имя пользователя или его id:\n')
                    correct_input = True
                else:
                    print('Некорректная команда. Повторите ввод')
    #Получение списка друзей
    response_friends_list = requests.get(
        'https://api.vk.com/method/friends.get',
        params={
            'access_token': TOKEN,
            'user_id': user_id,
            'v': 5.103
        }
    )
    #получение ID друзей
    ids = str(response_friends_list.json()['response']['items'][0])
    for first_user_friend in response_friends_list.json()['response']['items'][1:]:
        ids = ids + ', ' + str(first_user_friend)
    #Получение списка групп целевого пользователя и составление списка словарей групп
    response_user_groups = requests.get(
        'https://api.vk.com/method/groups.get',
        params={
            'access_token': TOKEN,
            'user_id': response_id.json()['response'][0]['id'],
            'extended': 1,
            # 'fields': 'member_count', не работает!
            'v': 5.103
        }
    )
    pprint(response_user_groups.json())
    user_group_list = []
    group_count = 0
    for user_group in response_user_groups.json()['response']['items']:
        group_count += 1
        print(f'Проверено сообществ: {group_count}/{len(response_user_groups.json()["response"]["items"])}')
        time.sleep(1)
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
        #проверка наличия друзей в группе?
        friend_member = 0
        try:
            for user_membership in response_mutual_groups.json()['response']:
                if user_membership['member'] == 1:
                    friend_member += 1
            if friend_member <= maxpeople:
                user_group_list.append({'name': user_group['name'], 'gid': user_group['id']})
        except KeyError:
            pass



    return user_group_list

APP_ID = 7423649
TOKEN = ''

check_bool = False
while not check_bool:
    token_check = requests.get(
        'https://api.vk.com/method/users.get',
        params={
            'access_token': TOKEN,
            'v': 5.103
        }
    )
    try:
        error_code_5 = token_check.json()['error']
        OAUTH_URL = 'https://oauth.vk.com/authorize'
        OAUTH_PARAMS = {
            'client_id': APP_ID,
            'display': 'page',
            'scope': 'groups,friends',
            'response_type': 'token',
            'v': 5.52
        }
        print('?'.join((OAUTH_URL, urlencode(OAUTH_PARAMS))))
        TOKEN = input('Пожалуйста, пройдите по ссылке и вставьте корректный TOKEN:\n')
    except KeyError:
        check_bool = True

username = input('Пожалуйста, введите имя пользователя или его id:\n')
spy_report = {'report': solitary_group(username)}

with open('groups.json', 'w') as report_file:
    json.dump(spy_report, report_file)

# проверка .json файла
# with open('groups.json') as json_check:
#     json_in_file = json.load(json_check)
#     pprint(json_in_file)