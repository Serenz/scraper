SUBITO_URL = 'https://www.subito.it/annunci-italia/vendita/'

SUBITO_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
    'device-memory': '8',
    'ect': '4g',
    'priority': 'u=0, i',
    'referer': 'https://www.subito.it/',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    # 'cookie': 'displayCookieConsent=y; user_data={"id":"109758064","email":"ced865970db52f42534b85ee759a60ab27b8c52ee3d1d9f57496ebd5fbf72982","name":"Marco","ppid":"4bca42a3251df94549cb04440bc8ee4e"}; didomi_token=eyJ1c2VyX2lkIjoiMThiZjcwOGMtN2RmNC02NDVmLTg0YTgtOTAyMDQ1MjI3ODNlIiwiY3JlYXRlZCI6IjIwMjMtMTEtMjJUMTI6Mzc6MDkuODc0WiIsInVwZGF0ZWQiOiIyMDI0LTExLTI1VDE0OjM1OjQ1LjE5MVoiLCJ2ZXJzaW9uIjoyLCJwdXJwb3NlcyI6eyJlbmFibGVkIjpbImNvb2tpZWFuYS1rQ0NSR3o0bSIsImNvb2tpZWRpLW5OZTIzUWpkIiwiY29va2lldGVjLTlxZkFFVndrIiwiYXVkaWVuY2VtLXhlZGVVMmdRIiwicHJveGltaXR5LUpEWFdkaGphIiwiZ2VvbG9jYXRpb25fZGF0YSIsImRldmljZV9jaGFyYWN0ZXJpc3RpY3MiXX0sInB1cnBvc2VzX2xpIjp7ImVuYWJsZWQiOlsicHJveGltaXR5LUpEWFdkaGphIl19LCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzphbXBsaXR1ZGUiLCJjOm1pY3Jvc29mdC1vbmVkcml2ZS1saXZlLXNkayIsImM6YXBwc2ZseWVyLTlqY3duaVk5IiwiYzpiaW5nLWFkcyIsImM6ZGlkb21pIiwiYzpwaW50ZXJlc3QiLCJjOmtydXgtZGlnaXRhbCIsImM6cXVhbnRjYXN0LW1lYXN1cmVtZW50IiwiYzpvbW5pdHVyZS1hZG9iZS1hbmFseXRpY3MiLCJjOmdyYXBlc2hvdCIsImM6cXVhbnR1bS1hZHZlcnRpc2luZyIsImM6eDEiLCJjOnR1YmVtb2d1bCIsImM6c2VnbWVudCIsImM6YWRtb2IiLCJjOm1lZGFsbGlhLWloenJ5RkxZIiwiYzpzYWxlc2ZvcmNlLUNQQkZFZkhQIiwiYzpvcHRpbWl6ZWx5LUVOUUVpaVpUIiwiYzpha2FjZG9yb2QtV0FEN2lYdGgiLCJjOm1pY3Jvc29mdC1hbmFseXRpY3MiLCJjOmF0aW50ZXJuZS1jV1FLSGVKWiIsImM6Ymx1ZWthaSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzpzb2Npb21hbnRpLW1NVEc4eGc0IiwiYzphd3MtY2xvdWRmcm9udCIsImM6bmV4dG1lZGlhLThHS2JmSmczIiwiYzpzdWJsaW1lc2stcFo3QW55N0ciLCJjOm1lZXRyaWNzZy1OZEVOOFd4VCIsImM6Y2VudHJvLWlVV1ZtTjROIiwiYzptaWNyb3NvZnQiLCJjOmhhdmFzbWVkaS1CQUc3cEpEZSIsImM6cm9ja2V0LWZ1ZWwiLCJjOnJhZGl1bW9uZSIsImM6YWR2ZXJ0aXNpbmdjb20iLCJjOnlhaG9vLWFkLWV4Y2hhbmdlIiwiYzp5YWhvby1hbmFseXRpY3MiLCJjOnlhaG9vLWFkLW1hbmFnZXItcGx1cyIsImM6YWRwaWxvdGNvbm5lY3RhZCIsImM6YnJpZ2h0cm9sbCIsImM6YWthbWFpLWNvb2tpZS1zeW5jIiwiYzphY2NvcmRhbnQtbWVkaWEiLCJjOmFvbC1jZG4iLCJjOnR1cmJvIiwiYzp0aWt0b2stS1pBVVFMWjkiLCJjOnlhaG9vLWdlbWluaS1hbmQtZmx1cnJ5IiwiYzpzcG90eGluYy13aUNFZkx5biIsImM6bWVkaWFtYXRoLXdKUXdUQVoyIl19LCJ2ZW5kb3JzX2xpIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpzb2Npb21hbnRpLW1NVEc4eGc0IiwiYzpuZXh0bWVkaWEtOEdLYmZKZzMiLCJjOmNlbnRyby1pVVdWbU40TiIsImM6aGF2YXNtZWRpLUJBRzdwSkRlIiwiYzp0dXJibyJdfSwiYWMiOiJEQnlBWUFFWUFMSUNTd0pSQVVWQkxHQ2VjRkNNTFJndEhCZWlEQmNHRGdBQS5EQnlBWUFFWUFMSUNTd0pSQVVWQkxHQ2VjRkNNTFJndEhCZWlEQmNHRGdBQSJ9; euconsent-v2=CP1pK0AQIpWwAAHABBENBRFsAP_gAEPgABCYJ9EB5C5cASNCAGp0AOsQAYUHQFAAAkAABAIBASABAIIAIIQEgGAQIAAAAAAAAAIAICYAAAAgAAAAAQAAAAAAIAEAAACQBAAAIAAAAAABAQAAAAAAAIAAEAAAgEAAAAAAgAAAAAIACEgAAAAAAAAAAAAAAAAFAAAAAAAAAAAIAAAIACgEAAAAAAAAAAAAABAIBAAAAAAEAAAAAAAAAAAAAAEEb4EIACwAKgAXAA4AB4AEEAMQAyABoAEQAI4ATIAuAC6AGIAMwAegA_ACEAEcAMoAfoBCACLQEcAR0AvoB7QExAKbAXmAwQBk4DLAH7gRvAAA.f_wACHwAAAAA; cmp_consent=1; _ga=GA1.1.1684780478.1733865948; _pin_unauth=dWlkPU9XRTNPRFEyTldZdE5qSm1NeTAwTXpNMUxUa3dOV0l0T0RFME5ESTRZV1poWldFdw; FPID=FPID2.2.TDdJWhALlgkbiVhySRK0XuQDBo3VC94Fq9CkAevKwQE%3D.1733865948; kampyle_userid=92f9-dccf-5b28-9cc6-9c14-efde-259a-5625; kampyleUserSession=1733865950638; kampyleUserSessionsCount=1; __gsas=ID=f32181e364ef8a67:T=1733866007:RT=1733866007:S=ALNI_MZFX9359kIrasTeTwu5wLX-okT3iw; kampyleUserPercentile=48.2777441563913; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22mrRzIu9dDIBpCXvTiq4C%22%2C%22expiryDate%22%3A%222025-12-10T21%3A35%3A02.986Z%22%7D; _ga_D72SGH4DYJ=GS1.1.1733865947.1.1.1733866502.0.0.2003891200; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22109758064%22%2C%22expiryDate%22%3A%222025-12-10T21%3A35%3A03.053Z%22%7D; _ga_XXXXXXXXXX=GS1.1.1733865947.1.1.1733866503.0.0.2050585742; _pulse2data=e5ccd4a6-c7b1-487b-84c2-b493a0fa0718%2Cv%2C109758064%2C1733867403151%2CeyJpc3N1ZWRBdCI6IjIwMjQtMTItMTBUMjE6MjU6NDdaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ.._FCSi9OtD7gHYXkhd2kw7g.Ysy9d5ba-Jg7f8Bh1W6jB5HeRlikdjBuPuC2ispM8AoHAgKsdfBfS2RQDb3inqOToloYej4S9o-8krAIdayLVr_W65nTiUV7tI2B6dfv7XyOYGJC-cyIi1JIPCXWLIS_WN6X779WIcx18aDPmVqd7FHAeQlNuS-kvj9SPLf_RsTdlvvjyfx3_XbNXyXtg7C4WQb6m-S-xYhMxb6DAXk9LP4LdGBkN2bobuGSYn7Gfns.qS27fvi8rzTVn7IeuZOoiQ%2C%2C%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..PaHqgLC9kKOH4gHzaZfLpUFyKDu2tbDpZs9uA2fRhRE; kampyleSessionPageCounter=4; __gads=ID=7e354a44758267e9:T=1733865946:RT=1733869001:S=ALNI_MZyuXp2V5QGkf-Hn_CGhGYOmAm99Q; __gpi=UID=00000f6ad4d0f95c:T=1733865946:RT=1733869001:S=ALNI_MaQqGRQQGCplO4ofrT4LW-70pIyeQ; akacd_orodha=2147483647~rv=48~id=44caa735336a96669ea4ba058f2ee7c0; kppid=A1FCA20A63C9BA7104E1404F',
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