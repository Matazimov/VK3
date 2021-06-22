from config import token, v
from .get_id import humans
from rich import print
import requests
import time
import os

if len(humans) > 0:
    print(f"[purple]У вас {len(humans)} новых заявок в друзья[/purple]\n"
          f"[cyan]Начинаю добавлять...[/cyan]")

    i = 0
    while i < len(humans):
        data = requests.post("https://api.vk.com/method/friends.add", params={
            "v": v,
            "user_id": humans[i],
            "access_token": token
        }).json()
        if "response" in data:
            print(f"[blue]id{humans[i]}[/blue]: Принял")
        elif "error" in data:
            if data["error"]["error_code"] == 1:
                print("[green]Лимит на добавления в друзья[/green]")
                time.sleep(1)
                os.system("python start.py")
            elif data["error"]["error_code"] == 29:
                print('[red]Достигнут количественный лимит на вызов метода[/red]'
                      'Подробнее об ограничениях на количество вызовов см. на странице '
                      'https://vk.com/dev/data_limits')
                time.sleep(1)
                os.system('python start.py')
            print(f"[blue]id{humans[i]}[/blue]: Пользователь заблокирован/удален")
        else:
            print("упс... произошла неизвестная ошибка")
            time.sleep(1)
            os.system('python start.py')
        i += 1
    print("[green]Все![/green]")
    time.sleep(1)
    os.system("python start.py")
else:
    print("[red]У вас нет новых заявок в друзья[/red]")
    time.sleep(1)
    os.system('python start.py')
