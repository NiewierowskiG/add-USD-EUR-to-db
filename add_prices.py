import mysql.connector
import pandas as pd
import NBPApi
import openpyxl


class AddPrices():
    def __init__(self, host, login, password, database):
        self.host = host
        self.login = login
        self.password = password
        self.database = database

    def connect(self):
        return mysql.connector.connect(
                host=self.host,
                user=self.login,
                password=self.password,
                database=self.database
        )

    def update(self):
        db = self.connect()
        cursor = db.cursor()
        #alter_command = "ALTER TABLE Product ADD UnitPriceUSD DECIMAL NOT NULL ; " \
        #                "ALTER TABLE Product ADD UnitPriceEuro DECIMAL NOT NULL ; "
        try:
            alter_command = "select UnitPriceEuro, UnitPriceEuro from Product"
            cursor.execute(alter_command)
        except mysql.connector.errors.ProgrammingError as e:
            if "Unknown column " in e.msg:
                alter_command = "ALTER TABLE Product ADD UnitPriceUSD DECIMAL NOT NULL ; " \
                                "ALTER TABLE Product ADD UnitPriceEuro DECIMAL NOT NULL ; "
                cursor.execute(alter_command)
        db = self.connect()
        cursor = db.cursor()
        df = pd.read_sql('select ProductID, UnitPrice from Product', con=db)
        update_rows = []
        exchange_rates = NBPApi.get_usd_eur_exchange_rate()
        for i in df.iterrows():
            update_rows.append((round(i[1]['UnitPrice'] / exchange_rates["EUR"]),
                               round(i[1]['UnitPrice'] / exchange_rates["USD"]),
                               i[1]['ProductID']
                               ))
        cursor.executemany("Update Product Set UnitPriceEuro = %s, UnitPriceUSD = %s where ProductID = %s", update_rows)
        db.commit()

    def to_excel(self):
        db = self.connect()
        df = pd.read_sql('select ProductID, DepartmentID, Category, IDSKU, ProductName, Quantity, UnitPrice, UnitPriceUSD,'
                         ' UnitPriceEuro, Ranking, ProductDesc, UnitsInStock, UnitsInOrder from Product', con=db)
        df.to_excel("output.xlsx")
