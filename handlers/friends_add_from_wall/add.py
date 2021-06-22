from config import token, v
from .get_id import humans
from rich import print
import requests
import time
import os

if len(humans) > 0:
    print(f"[purple]Удалось получить {len(humans)} пользователей[/purple]")
    print("[cyan]Начинаю добавлять...[/cyan]")
    i = 0
    while i < len(humans):
        data = requests.post("https://api.vk.com/method/friends.add", params={
            "v": v,
            "access_token": token,
            "user_id": humans[i]
        }).json()
        if "response" in data:
            if data['response'] == 1:
                print(f"[blue]id{humans[i]}[/blue]: Добавил")
            elif data['response'] == 2:
                print(f"[blue]id{humans[i]}[/blue]: Уже в друзьях")
            else:
                print(f"[blue]id{humans[i]}[/blue]: Добавил")
        elif "error" in data:
            if data['error']["error_code"] == 14:
                captcha_sid = data['error']["captcha_sid"]
                print(f"Введите код с капчи:\nhttps://api.vk.com/captcha.php?"
                      f"sid={captcha_sid}")
                code = input()
                data_captcha = requests.post('https://api.vk.com/method/friends.add', params={
                    'v': v,
                    'captcha_key': code,
                    'user_id': humans[i],
                    'access_token': token,
                    'captcha_sid': captcha_sid
                }).json()
                if "response" in data_captcha:
                    print("[green]Верно[/green]\n"
                          f"[blue]id{humans[i]}[/blue]: Добавил")
                elif "error" in data_captcha:
                    if data_captcha["error"]["error_code"] == 14:
                        print("[red]Неверно[/red]")
                else:
                    print("упс... произошла неизвестная ошибка")
                    time.sleep(1)
                    os.system('python start.py')
            elif data["error"]["error_code"] == 1:
                print("[green]Лимит на добавления в друзья[/green]")
                time.sleep(2)
                os.system("python start.py")
            elif data["error"]["error_code"] == 29:
                print('[red]Достигнут количественный лимит на вызов метода[/red]'
                      'Подробнее об ограничениях на количество вызовов см. на странице '
                      'https://vk.com/dev/data_limits')
                time.sleep(1)
                os.system('python start.py')
        else:
            print("упс... произошла неизвестная ошибка")
            time.sleep(1)
            os.system('python start.py')
        i += 1
    print("[green]Все![/green]")
    time.sleep(1)
    os.system("python start.py")
else:
    print("[red]В этой странице/группе нету записей[/red]")
    time.sleep(1)
    os.system('python start.py')
