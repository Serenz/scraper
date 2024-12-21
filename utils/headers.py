SUBITO_URL = 'https://www.subito.it/annunci-italia/vendita/'

SUBITO_HEADERS = headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'upgrade-insecure-requests': '1',
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

EBAY_HEADERS = {
    'Referer': 'https://www.ebay.com/b/Vintage-Electronic-Drums/181174/bn_16566434?LH_BIN=1&LH_ItemCondition=4%7C10&mag=1&rt=nc',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-full-version': '"131.0.6778.205"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
}

EBAY_PARAMS = {
    'LH_BIN': '1',
    'LH_ItemCondition': '4|10',
    '_sop': '10',
    'mag': '1',
    'rt': 'nc',
}