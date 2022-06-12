import sys
import add_prices

if __name__ == "__main__":
    i = 1
    excel = False
    host = "localhost"
    login = "root"

    while i < len(sys.argv):
        if sys.argv[i] == "--host":
            host = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--login":
            login = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--password":
            password = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--database":
            database = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == "--excel":
            excel = True
            excel_filename = sys.argv[i+1]
            i += 2
        else:
            print(f"Błędny parametr {sys.argv[i]}")
            i += 1
    db = add_prices.AddPrices(host, login, password, database)
    db.update()
    if excel:
        db.to_excel(excel_filename)

