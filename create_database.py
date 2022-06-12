import mysql.connector
from urllib.request import urlopen
import time

db = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='admin'
)
url = 'https://raw.githubusercontent.com/abdelatifsd/E-commerce-Database-Project/master/3%20-%20Structure.sql'
sql_commands = urlopen(url).read().decode("utf-8")
cursor = db.cursor()
cursor.execute(sql_commands)
url = 'https://raw.githubusercontent.com/abdelatifsd/E-commerce-Database-Project/master/4%20-%20Population.sql'
sql_commands = urlopen(url).read().decode('utf-8')
tmp = sql_commands.split('COMMIT;')
for command in tmp:
    cursor.close()
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='admin'
    )
    time.sleep(1)
    cursor = db.cursor()
    print(command + "COMMIT;")
    cursor.execute(command + "COMMIT;")

