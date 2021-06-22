from config import token, v, first_name, last_name
from rich import print
from cls import cls
import requests
import time
import os

cls()
owner_id = input(f"({first_name} {last_name}) Введите id группы: ")


def get_comment():
    data = requests.get("https://api.vk.com/method/wall.get", params={
        "v": v,
        "count": 1,
        "filter": "others",
        "access_token": token,
        "owner_id": owner_id
    }).json()

    if "response" not in data:
        print("[red]Произошла ошибка[/red]")
        time.sleep(1)
        os.system('python start.py')

    return data


if get_comment()['response']['count'] == 0:
    print('[red]Такое сообщество не существует[/red]')
    time.sleep(1)
    os.system('python start.py')

cls()
message = input(f"({first_name} {last_name}) Введите коммент: ")
cls()
print("[yellow]Начинаю работать...[/yellow]")


while True:
    answer = get_comment()['response']['items'][0]['id']
    human = get_comment()['response']['items'][0]['from_id']

    data_true = requests.get('https://api.vk.com/method/users.get', params={
        'v': v,
        'access_token': token,
        'fields': 'is_friend',
        'user_ids': human
    }).json()

    if data_true['response'][0]['is_friend'] == 0:
        comment = requests.post('https://api.vk.com/method/wall.createComment', params={
            "owner_id": owner_id,
            'post_id': answer,
            'v': v,
            'access_token': token,
            'message': message
        }).json()
        if 'response' in comment:
            if comment['response'] == 212 or 213:
                print('[red]Нет доступа к комментированию записи[/red]')
            elif comment['response'] == 222:
                print('[red]Запрещено размещение ссылок в комментариях[/red]')
            elif comment['response'] == 223:
                print('[red]Превышен лимит комментариев на стене[/red]')
            else:
                print(f'[blue]{answer}[/blue]: Оставил')
        elif "error" in comment:
            if comment['error']["error_code"] == 14:
                captcha_sid = comment['error']["captcha_sid"]
                print(f"Введите код с капчи:\nhttps://api.vk.com/captcha.php?"
                      f"sid={captcha_sid}")
                code = input()
                comment_captcha = requests.post('https://api.vk.com/method/wall.createComment', params={
                    'v': v,
                    'access_token': token,
                    'post_id': answer,
                    "owner_id": owner_id,
                    'message': message,
                    'captcha_sid': captcha_sid,
                    'captcha_key': code
                }).json()
                if "response" in comment_captcha:
                    print("[green]Верно[/green]\n"
                          f"[blue]id{answer}[/blue]: Оставил")
                elif "error" in comment_captcha:
                    if comment_captcha["error"]["error_code"] == 14:
                        print("[red]Неверно[/red]")
                else:
                    print("упс... произошла неизвестная ошибка")
                    time.sleep(1)
                    os.system('python start.py')
            elif comment["error"]["error_code"] == 29:
                print('[red]Достигнут количественный лимит на вызов метода[/red]'
                      'Подробнее об ограничениях на количество вызовов см. на странице '
                      'https://vk.com/dev/data_limits')
                time.sleep(1)
                os.system('python start.py')
        else:
            print("упс... произошла неизвестная ошибка")

    time.sleep(1)
