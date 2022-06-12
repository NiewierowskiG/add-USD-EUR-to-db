import mysql.connector
import pandas as pd
import NBPApi
import logging
import os

current_filename = os.path.basename(__file__).rsplit('.', 1)[0]
logging.basicConfig(filename=current_filename + '.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


class AddPrices():
    def __init__(self, host, login, password, database):
        self.host = host
        self.login = login
        self.password = password
        self.database = database

    def connect(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.login,
                password=self.password,
                database=self.database
            )
        except mysql.connector.errors.ProgrammingError as e:
            logging.error(e.msg)
        except mysql.connector.errors.DatabaseError as e:
            logging.error(e.msg)

    def update(self):
        db = self.connect()
        cursor = db.cursor()
        try:
            alter_command = "select UnitPriceEuro, UnitPriceEuro from Product"
            cursor.execute(alter_command)
        except mysql.connector.errors.ProgrammingError as e:
            if "Unknown column " in e.msg:
                alter_command = "ALTER TABLE Product ADD UnitPriceUSD DECIMAL NOT NULL;" \
                                "ALTER TABLE Product ADD UnitPriceEuro DECIMAL NOT NULL;"
                cursor.execute(alter_command)
                logging.info(alter_command.split(';')[0])
                logging.info(alter_command.split(';')[1])

        db = self.connect()
        cursor = db.cursor()
        df = pd.read_sql('select ProductID, UnitPrice from Product', con=db)
        update_rows = []
        try:
            exchange_rates = NBPApi.get_usd_eur_exchange_rate()
        except NBPApi.NBPApiError as e:
            logging.error(e.msg)
        for i in df.iterrows():
            update_rows.append((round(i[1]['UnitPrice'] / exchange_rates['EUR']),
                               round(i[1]['UnitPrice'] / exchange_rates["USD"]),
                               i[1]['ProductID']
                               ))
        try:
            cursor.executemany("Update Product Set UnitPriceEuro = %s, UnitPriceUSD = %s where ProductID = %s", update_rows)
            db.commit()
            for row in update_rows:
                logging.info(f"Update Product Set UnitPriceEuro = {row[0]}, UnitPriceUSD = {row[1]} where ProductID = {row[2]}")
        except mysql.connector.errors.ProgrammingError as e:
            logging.error(e.msg)
        except mysql.connector.errors.DatabaseError as e:
            logging.error(e.msg)


    def to_excel(self):
        db = self.connect()
        df = pd.read_sql('select ProductID, DepartmentID, Category, IDSKU, ProductName, Quantity, UnitPrice, UnitPriceUSD,'
                         ' UnitPriceEuro, Ranking, ProductDesc, UnitsInStock, UnitsInOrder from Product', con=db)

        df.to_excel("output.xlsx")
