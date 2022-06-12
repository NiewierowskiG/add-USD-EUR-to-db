import requests


class NBPApiError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.message


def get_usd_eur_exchange_rate():
    response1 = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/eur/')
    response2 = requests.get('http://api.nbp.pl/api/exchangerates/rates/a/usd/')
    if response2.status_code != 200 or response1.status_code != 200:
        raise NBPApiError("Problem with connecting to NBP api servers")
    eur = response1.json()['rates'][0]['mid']
    usd = response2.json()['rates'][0]['mid']
    return {"EUR": eur, "USD": usd}
