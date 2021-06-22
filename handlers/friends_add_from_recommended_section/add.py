from .get_id import humans
from config import token, v
from rich import print
import requests
import time
import os

if len(humans) > 0:
    print(f"Вконтакте вернул {len(humans)} рекомендованных друзей")
    print("[cyan]Начинаю добавлять...[/cyan]")
    i = 0
    while i < len(humans):
        data = requests.post("https://api.vk.com/method/friends.add", params={
            "v": v,
            "access_token": token,
            "user_id": humans[i]["id"]
        }).json()
        if "response" in data:
            print(f"[blue]id{humans[i]['id']}[/blue]: Добавил")
        elif "error" in data:
            if data['error']["error_code"] == 14:
                captcha_sid = data['error']["captcha_sid"]
                print(f"Введите код с капчи:\nhttps://api.vk.com/captcha.php?"
                      f"sid={captcha_sid}")
                code = input()
                data_captcha = requests.post('https://api.vk.com/method/friends.add', params={
                    'user_id': humans[i]["id"],
                    'v': v,
                    'access_token': token,
                    'captcha_sid': captcha_sid,
                    'captcha_key': code
                }).json()
                if "response" in data_captcha:
                    print("[green]Верно[/green]")
                    print(f"[blue]id{humans[i]['id']}[/blue]: Добавил")
                elif "error" in data_captcha:
                    if data_captcha["error"]["error_code"] == 14:
                        print("[red]Неверно[/red]")
                else:
                    print("упс... произошла неизвестная ошибка")
                    time.sleep(1)
                    os.system('python start.py')
            elif data["error"]["error_code"] == 1:
                print("[green]Лимит на добавления в друзья[/green]")
                time.sleep(1)
                os.system('python start.py')
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
    os.system('python start.py')
else:
    print("[red]Вконтакте пока что не подготовил рекомендованных друзей(([/red]")
    time.sleep(1)
    os.system('python start.py')
