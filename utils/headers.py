SUBITO_URL = 'https://www.subito.it/hades/v1/search/items'

SUBITO_HEADERS = {
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

MERCATINO_URL = 'https://www.mercatinomusicale.com/ann/search.asp'

MERCATINO_HEADERS = {
    'authority': 'www.mercatinomusicale.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
    'referer': 'https://www.mercatinomusicale.com/tastiere/',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
}

MERCATINO_ID_PATTERN = r"_id(\d+)\.html"