import requests


def get_usd_eur_exchange_rate():
    response = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/eur/').json()
    eur = response['rates'][0]['mid']
    response = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/').json()
    usd = response['rates'][0]['mid']
    return {"EUR": eur, "USD": usd}
