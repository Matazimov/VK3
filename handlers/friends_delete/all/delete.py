from config import token, v
from .get_id import humans
from rich import print
import requests
import os
import time

if len(humans) > 0:
    print(f"[purple]У вас {len(humans)} друзей[/purple]")
    confirm = input("Удалить всех друзей? [Да/Нет] ")
    if confirm.lower() == "да":
        print("[cyan]Начинаю удалять...[/cyan]")
    elif confirm.lower() == "нет":
        print("[red]Действие отменено[/red]")
        time.sleep(1)
        os.system('python start.py')
    else:
        print("[red]Выберите только из предложенных вариантов[/red]")
        time.sleep(1)
        os.system('python start.py')

    i = 0
    while i < len(humans):
        data = requests.post("https://api.vk.com/method/friends.delete", params={
            "v": v,
            "user_id": humans[i],
            "access_token": token
        }).json()
        if "response" in data:
            print(f"[blue]id{humans[i]}[/blue]: Удалил")
        elif "error" in data:
            if data["error"]["error_code"] == 29:
                print('[red]Достигнут количественный лимит на вызов метода[/red]'
                      'Подробнее об ограничениях на количество вызовов см. на странице '
                      'https://vk.com/dev/data_limits')
                time.sleep(1)
                os.system('python start.py')
            print(f"[blue]id{humans[i]}[/blue]: Не смог удалить")
        else:
            print("упс... произошла неизвестная ошибка")
            time.sleep(1)
            os.system('python start.py')
        i += 1
    print("[green]Все![/green]")
    time.sleep(1)
    os.system('python start.py')
else:
    print("[red]У вас 0 друзей[/red]")
    time.sleep(1)
    os.system('python start.py')
