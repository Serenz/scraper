import requests
import json

headers = {
    'authority': 'www.subito.it',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
    'referer': 'https://www.subito.it/_next/static/chunks/946.902eb56b34a9b858.js',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'x-subito-channel': 'web',
    'x-subito-environment-id': '',
}

params = {
    'q': 'iphone 12',
    'c': '',
    't': 's',
    'qso': 'false',
    'shp': 'false',
    'urg': 'false',
    'sort': 'datedesc',
    'lim': '1',
    'start': '0',
}

response = requests.get('https://www.subito.it/hades/v1/search/items', params=params, headers=headers)
j = response.json()
print(json.dumps(j, indent=4))

# response = requests.get('https://www.subito.it/hades/v1/search/items', params=params, headers=headers)
# j = response.json()
# with open('p.txt', 'w') as f:
#     f.writelines(json.dumps(j, indent=4))
# print(json.dumps(j, indent=4))
# print(j['filters']['c'])


# mapping = dict()

# for _ in range(0, 100):
#     params['r'] = _
#     try:
#         response = requests.get('https://www.subito.it/hades/v1/search/items', params=params, headers=headers)
#         j = response.json()
#         mapping[_] = j['filters']['r']
#     except:
#         print(f'Fermato a {_}')
#         break

# with open('regions_mapping.txt', 'w') as f:
#     json.dump(mapping, f, indent=4)