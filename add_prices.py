import mysql.connector
import pandas as pd
import NBPApi


class AddPrices():
    def __init__(self, host, login, password, database):
        try:
            self.db = mysql.connector.connect(
                host=host,
                user=login,
                password=password,
                database=database
            )
        except:
            print("eo")
            pass

    def update(self):
        cursor = self.db.cursor()
        try:
            alterCommand = "ALTER TABLE Product ADD UnitPriceUSD DECIMAL NOT NULL; " \
                           "ALTER TABLE Product ADD UnitPriceEuro DECIMAL NOT NULL; "
            cursor.execute(alterCommand)
        except:
            pass
        df = pd.read_sql('select ProductID, UnitPrice from Product', con=self.db)
        updateRows = []
        exchange_rates = NBPApi.get_usd_eur_exchange_rate()
        for i in df.iterrows():
            updateRows.append((round(i[1]['UnitPrice'] / exchange_rates["EUR"]),
                               round(i[1]['UnitPrice'] / exchange_rates["USD"]),
                               i[1]['ProductID']
                               ))
        cursor.executemany("Update Product Set UnitPriceEuro = %s, UnitPriceUSD = %s where ProductID = %s", updateRows)
        self.db.commit()
