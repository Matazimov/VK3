from rich.console import Console
from rich.table import Table
from rich import print
from cls import cls
import sqlite3
import sys


cls()

v = 5.131

try:
    conn = sqlite3.connect('accounts.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM accounts")

    table = Table(header_style="bold magenta", border_style="green", title="Аккаунты:")
    table.add_column("id")
    table.add_column("Имя Фамилия")

    while True:
        row = cur.fetchone()
        if row == None:
            break
        table.add_row(
            f"{row[3]}",
            f"{row[0]} {row[1]}"
        )

    console = Console()
    console.print(table)

    user_id = input("Введите id: ")
    cur.execute(f"SELECT * FROM accounts WHERE id = {user_id}")
    select_account = cur.fetchone()

    first_name = select_account[0]
    last_name = select_account[1]
    token = select_account[2]
except:
    print('[red]Нет аккаунтов[/red]')
    sys.exit()
