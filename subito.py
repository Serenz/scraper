import requests
import json

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.subito.it/_next/static/chunks/946.902eb56b34a9b858.js',
    'X-Subito-Environment-ID': '',
    'X-Subito-Channel': 'web',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

params = {
    'q': 'iphone 12', #oggetto
    #'c': '9' #categoria -> numero = categoria (9=Elettronica)
    't': 's', #(s/g/k) -> s: in vendita. g: in regalo. k: cercasi
    #'r': 'numero' -> senza 'r' = tutta italia
    'qso': 'false', #cerca solo nel titolo (true/false)
    'shp': 'false', #spedizione disponibile (ture/false)
    'urg': 'false', #annunci urgenti (true/false)
    'sort': 'datedesc', #(relevance/datadesc/priceasc/pricedesc) priceasc = dal meno caro
    'lim': '1',
    'start': '0',
}

response = requests.get('https://www.subito.it/hades/v1/search/items', params=params, headers=headers)
j = response.json()
with open('decode.txt', 'w') as f:
    json.dump(j, f, indent=4)
# print(json.dumps(j, indent=4))
