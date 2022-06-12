import mysql.connector
from urllib.request import urlopen
import sys

if __name__ == "__main__":
    host = "localhost"
    login = "root"
    password = "admin"
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--host":
            host = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--login":
            login = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--password":
            password = sys.argv[i + 1]
            i += 2
    db = mysql.connector.connect(
        host=host,
        user=login,
        password=password
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
        cursor = db.cursor()
        cursor.execute(command + "COMMIT;")
