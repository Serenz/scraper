import requests
import json

headers = {
    'authority': 'www.subito.it',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
    # 'cookie': 'kppid=A49B5D0434A5BE2E95AAC5A7; didomi_token=eyJ1c2VyX2lkIjoiMThiZjcwOGMtN2RmNC02NDVmLTg0YTgtOTAyMDQ1MjI3ODNlIiwiY3JlYXRlZCI6IjIwMjMtMTEtMjJUMTI6Mzc6MDkuODc0WiIsInVwZGF0ZWQiOiIyMDIzLTExLTIyVDEyOjM3OjQ0LjAzOFoiLCJ2ZXJzaW9uIjoyLCJwdXJwb3NlcyI6eyJlbmFibGVkIjpbImNvb2tpZWFuYS1rQ0NSR3o0bSIsImNvb2tpZWRpLW5OZTIzUWpkIiwiY29va2lldGVjLTlxZkFFVndrIiwiYXVkaWVuY2VtLXhlZGVVMmdRIiwicHJveGltaXR5LUpEWFdkaGphIiwiZ2VvbG9jYXRpb25fZGF0YSJdfSwicHVycG9zZXNfbGkiOnsiZW5hYmxlZCI6WyJwcm94aW1pdHktSkRYV2RoamEiXX0sInZlbmRvcnMiOnsiZW5hYmxlZCI6WyJnb29nbGUiLCJjOmFtcGxpdHVkZSIsImM6bWljcm9zb2Z0LW9uZWRyaXZlLWxpdmUtc2RrIiwiYzphcHBzZmx5ZXItOWpjd25pWTkiLCJjOmJpbmctYWRzIiwiYzpkaWRvbWkiLCJjOnBpbnRlcmVzdCIsImM6a3J1eC1kaWdpdGFsIiwiYzpxdWFudGNhc3QtbWVhc3VyZW1lbnQiLCJjOm9tbml0dXJlLWFkb2JlLWFuYWx5dGljcyIsImM6Z3JhcGVzaG90IiwiYzpxdWFudHVtLWFkdmVydGlzaW5nIiwiYzp4MSIsImM6dHViZW1vZ3VsIiwiYzpzZWdtZW50IiwiYzphZG1vYiIsImM6bWVkYWxsaWEtaWh6cnlGTFkiLCJjOnNhbGVzZm9yY2UtQ1BCRkVmSFAiLCJjOm9wdGltaXplbHktRU5RRWlpWlQiLCJjOmFrYWNkb3JvZC1XQUQ3aVh0aCIsImM6bWljcm9zb2Z0LWFuYWx5dGljcyIsImM6YXRpbnRlcm5lLWNXUUtIZUpaIiwiYzpwYW5nbGVkc3AtWkJ4TGhnQ1ciLCJjOmJsdWVrYWkiLCJjOmdvb2dsZWFuYS00VFhuSmlnUiIsImM6c29jaW9tYW50aS1tTVRHOHhnNCIsImM6YXdzLWNsb3VkZnJvbnQiLCJjOm5leHRtZWRpYS04R0tiZkpnMyIsImM6c3VibGltZXNrLXBaN0FueTdHIiwiYzptZWV0cmljc2ctTmRFTjhXeFQiLCJjOmNlbnRyby1pVVdWbU40TiIsImM6bWljcm9zb2Z0Il19LCJ2ZW5kb3JzX2xpIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpwYW5nbGVkc3AtWkJ4TGhnQ1ciLCJjOnNvY2lvbWFudGktbU1URzh4ZzQiLCJjOm5leHRtZWRpYS04R0tiZkpnMyIsImM6Y2VudHJvLWlVV1ZtTjROIl19LCJhYyI6IkRCZUFXQUZrQkpZRW9nSllnVVZCTEdDZWNGQ0lMUndYb2d3WC5EQmVBV0FGa0JKWUVvZ0pZZ1VWQkxHQ2VjRkNJTFJ3WG9nd1gifQ==; euconsent-v2=CP1pK0AP1pK0AAHABBENAbEoAP_gAELgABCYI3wPgABQAKAAwACAAFYALgAwABwADwAIAAWwAxADIAGkARABFACZAFsAXIAwgDEAGYAOQAeAA9QCAAIEAQgAjABHAChAFIAMEAZQA0gBxADxAH6AQgAiABEwCOAEtALSAXUAvsBgAGBAM6AcIA9oB-gELAIgARqAmIBTYCwwFmALzAYyAycBlgDmAHNAP3AgKBAcCMwEbwRvgQwAKAAsACoAFwAOAAeABBADEAMgAaABEACYAFwAMQAZgA9AB-AEIAI4AZQA_QCEAEWAI4AXUAvoB7QExAKbAXmAwQBk4DLAH7gRvAEFQAYAAiDUQgAwABEGoRABgACINQyADAAEQagA.f_wACFwAAAAA; displayCookieConsent=y; akacd_orodha=2177452799~rv=5~id=e8e63885ca2c67e0793ffe581f8c429e',
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
    'c': '9',
    't': 's',
    'qso': 'false',
    'shp': 'false',
    'urg': 'false',
    'sort': 'datedesc',
    'lim': '1',
    'start': '0',
}


# response = requests.get('https://www.subito.it/hades/v1/search/items', params=params, headers=headers)
# j = response.json()
# with open('p.txt', 'w') as f:
#     f.writelines(json.dumps(j, indent=4))
# print(json.dumps(j, indent=4))
# print(j['filters']['c'])
mapping = dict()

for _ in range(0, 100):
    params['r'] = _
    try:
        response = requests.get('https://www.subito.it/hades/v1/search/items', params=params, headers=headers)
        j = response.json()
        mapping[_] = j['filters']['r']
    except:
        print(f'Fermato a {_}')
        break

with open('regions_mapping.txt', 'w') as f:
    json.dump(mapping, f, indent=4)