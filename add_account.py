import requests
import sqlite3
import time
import sys
import os
from cls import cls
from rich import print

cls()

conn = sqlite3.connect('accounts.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS accounts(
    first_name TEXT,
    last_name TEXT,
    token TEXT,
    id TEXT
)''')
conn.commit()

token = input("Введите токен: ")


info = requests.get('https://api.vk.com/method/users.get', params={
        'v': 5.131,
        'name_case': 'Nom',
        'access_token': token,
        'fields': 'photo_max_orig,counters'
    }).json()
if "error" in info:
    print("[red]Неправильный токен[/red]")
    sys.exit()

first_name = info["response"][0]["first_name"]
last_name = info["response"][0]["last_name"]
user_id = info["response"][0]["id"]

user = (first_name, last_name, token, user_id)
cur.execute("INSERT INTO accounts VALUES(?, ?, ?, ?)", user)
conn.commit()
cur.execute("SELECT * FROM accounts")
print(f'{user_id}: [green]добавлен[/green]')
time.sleep(1)
os.system('python start.py')
