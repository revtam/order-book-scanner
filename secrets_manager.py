import json


with open('secrets.json') as f:
    data = json.load(f)


class Api_keys:
    kucoin_public = data["kucoin"]["api_key"]
    kucoin_private = data["kucoin"]["private_key"]
    kucoin_passphrase = data["kucoin"]["passphrase"]
