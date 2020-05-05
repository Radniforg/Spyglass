from pprint import pprint
from urllib.parse import urlencode
import requests
import json
import time


def token_confirmation(app_id):
    token = ''
    check_bool = False
    while not check_bool:
        token_check = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'access_token': token,
                'v': 5.103
            }
        )
        try:
            token = token_check.json()['error']
            OAUTH_URL = 'https://oauth.vk.com/authorize'
            OAUTH_PARAMS = {
                'client_id': app_id,
                'display': 'page',
                'scope': 'groups,friends',
                'response_type': 'token',
                'v': 5.52
            }
            print('?'.join((OAUTH_URL, urlencode(OAUTH_PARAMS))))
            token = input('Пожалуйста, пройдите по ссылке и'
                          ' вставьте корректный TOKEN:\n')
        except KeyError:
            check_bool = True
    return token


def user_confirmed(user1):
    # Получение id пользователя
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
                function_suspension = input('Некорректное имя пользователя. '
                                            'Хотите продолжить (Y/N):\n')
                if function_suspension.lower() == 'n':
                    return 'Программа остановлена пользователем. ' \
                           'Некорректное имя пользователя'
                elif function_suspension.lower() == 'y':
                    user1 = input('Пожалуйста, введите имя пользователя'
                                  ' или его id:\n')
                    correct_input = True
                else:
                    print('Некорректная команда. Повторите ввод')
    return user_id


def user_friends(user_id, max_friends=1000):
    # Получение списка друзей
    friend_count = 0
    friend_limit = 0
    response_friends_list = requests.get(
        'https://api.vk.com/method/friends.get',
        params={
            'access_token': TOKEN,
            'user_id': user_id,
            'v': 5.103
        }
    )
    # получение ID друзей
    pprint(response_friends_list.json())
    id_list = []
    ids = str(response_friends_list.json()['response']['items'][0])
    for user_friend in response_friends_list.json()['response']['items'][1:]:
        if friend_count == max_friends:
            break
        elif friend_count == 999:
            id_list.append(ids)
            friend_count = 0
            ids = str(user_friend)
        else:
            ids = ids + ', ' + str(user_friend)
        friend_count += 1
        friend_limit += 1
    id_list.append(ids)
    return id_list


def solitary_group(user_id, id_list, maxpeople=0, grouplimit=1000):
    # Получение списка групп целевого пользователя и
    # составление списка словарей групп
    response_user_groups = requests.get(
        'https://api.vk.com/method/groups.get',
        params={
            'access_token': TOKEN,
            'user_id': user_id,
            'extended': 1,
            'fields': 'members_count',
            'v': 5.103
        }
    )
    user_group_list = []
    group_count = 0
    for user_group in response_user_groups.json()['response']['items']:
        group_count += 1
        if group_count > grouplimit:
            print(f'Программа превысила лимит групп '
                  f'равный {grouplimit}, оставшиеся группы'
                  f' не будут проанализированы')
            break
        print(f'Проверено сообществ: {group_count}/'
              f'{len(response_user_groups.json()["response"]["items"])}')
        time.sleep(1)
        friend_member = 0
        for ids in id_list:
            response_mutual_groups = requests.get(
                'https://api.vk.com/method/groups.isMember',
                params={
                    'access_token': TOKEN,
                    'group_id': user_group['id'],
                    'user_ids': ids,
                    'extended': 1,
                    'v': 5.103
                }
            )
            # проверка наличия друзей в группе?
            try:
                for user_membership in\
                        response_mutual_groups.json()['response']:
                    if user_membership['member'] == 1:
                        friend_member += 1
            except KeyError:
                pass
        if friend_member <= maxpeople:
            user_group_list.append({'name': user_group['name'],
                                    'gid': user_group['id'],
                                    'members:': user_group['members_count']})
    return user_group_list


APP_ID = 7423649
TOKEN = token_confirmation(APP_ID)
username = input('Пожалуйста, введите имя пользователя или'
                 ' его id:\n')
spy_report = {'report': solitary_group(user_confirmed(username),
                                       user_friends(user_confirmed(username)))}

with open('groups.json', 'w') as report_file:
    json.dump(spy_report, report_file)

# проверка .json файла
with open('groups.json') as json_check:
    json_in_file = json.load(json_check)
    pprint(json_in_file)
