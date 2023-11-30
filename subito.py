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
    'lim': '30',
    'start': '0',
}

response = requests.get('https://www.subito.it/hades/v1/search/items', params=params, headers=headers)
j = response.json()
print(json.dumps(j, indent=4))




# import requests

# cookies = {
#     'datr': 'sGNhZF6QhjzJ_ZYReA3lEp_8',
#     'sb': 's2NhZFEf5A81NvcMko1HhdrM',
#     'c_user': '100002228794636',
#     'm_ls': '%7B%22c%22%3A%7B%221%22%3A%22HCwAABaK4gEWwuLBtQETBRaY1JfV8rwtAA%22%2C%222%22%3A%22GSwVQBxMAAAWARbu8OLRDBYAABV-HEwAABYAFu7w4tEMFgAAFigA%22%2C%2295%22%3A%22HCwAABYoFpTGnqQHEwUWmNSX1fK8LQA%22%7D%2C%22d%22%3A%222ee3f34a-4eb2-4a08-bf00-92ec3ffca749%22%2C%22s%22%3A%221%22%2C%22u%22%3A%225o71bp%22%7D',
#     'xs': '40%3A-dNgDgmZvs6eMw%3A2%3A1684104116%3A-1%3A10638%3A%3AAcU2Ema0B6Qjs133g5CmDm6JtkZSmP_uvDz5c5XeEw',
#     'fr': '1jDSIlXEunIgV2vtR.AWXW_cMujAk1RlVug3RP7akL8tg.BlYILm.jr.AAA.0.0.BlYILm.AWUi-YUHWt4',
#     'presence': 'C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1700824408751%2C%22v%22%3A1%7D',
#     'wd': '1336x1315',
# }

# headers = {
#     'authority': 'www.facebook.com',
#     'accept': '*/*',
#     'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6',
#     'content-type': 'application/x-www-form-urlencoded',
#     # 'cookie': 'datr=sGNhZF6QhjzJ_ZYReA3lEp_8; sb=s2NhZFEf5A81NvcMko1HhdrM; c_user=100002228794636; m_ls=%7B%22c%22%3A%7B%221%22%3A%22HCwAABaK4gEWwuLBtQETBRaY1JfV8rwtAA%22%2C%222%22%3A%22GSwVQBxMAAAWARbu8OLRDBYAABV-HEwAABYAFu7w4tEMFgAAFigA%22%2C%2295%22%3A%22HCwAABYoFpTGnqQHEwUWmNSX1fK8LQA%22%7D%2C%22d%22%3A%222ee3f34a-4eb2-4a08-bf00-92ec3ffca749%22%2C%22s%22%3A%221%22%2C%22u%22%3A%225o71bp%22%7D; xs=40%3A-dNgDgmZvs6eMw%3A2%3A1684104116%3A-1%3A10638%3A%3AAcU2Ema0B6Qjs133g5CmDm6JtkZSmP_uvDz5c5XeEw; fr=1jDSIlXEunIgV2vtR.AWXW_cMujAk1RlVug3RP7akL8tg.BlYILm.jr.AAA.0.0.BlYILm.AWUi-YUHWt4; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1700824408751%2C%22v%22%3A1%7D; wd=1336x1315',
#     'dpr': '1.5',
#     'origin': 'https://www.facebook.com',
#     'referer': 'https://www.facebook.com/marketplace/107933505906257/search/?query=iphone',
#     'sec-ch-prefers-color-scheme': 'dark',
#     'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
#     'sec-ch-ua-full-version-list': '"Google Chrome";v="119.0.6045.160", "Chromium";v="119.0.6045.160", "Not?A_Brand";v="24.0.0.0"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-model': '""',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-ch-ua-platform-version': '"15.0.0"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
#     'viewport-width': '1336',
#     'x-asbd-id': '129477',
#     'x-fb-friendly-name': 'CometMarketplaceSearchContentPaginationQuery',
#     'x-fb-lsd': 'sbOKxNYQWQx10QyR1V77Fw',
# }

# data = {
#     'av': '100002228794636',
#     '__user': '100002228794636',
#     '__a': '1',
#     '__req': '7s',
#     '__hs': '19685.HYP:comet_pkg.2.1..2.1',
#     'dpr': '1.5',
#     '__ccg': 'EXCELLENT',
#     '__rev': '1010026608',
#     '__s': 'g9yru8:76srms:5o71bp',
#     '__hsi': '7304982508247081759',
#     '__dyn': '7AzHK4HzEmgDx-5Q1ryaxG4QjFwLBwopU98nwgUao4ubyQdwSAxacyUco5S3O2Saxa1NwJwpUe8hw8u250n82nwb-q7oc81xoswIK1Rwwwg8a8465o-cw8a1TwgEcEhwGxu782lwj8bU9kbxS210hU31wiE567Udo5qfK0zEkxe2GexeeDwkUtxGm2SUbElxm3y11xfxmu3W3rwxwhFVovUy2a0SEuBwFKq2-azqwqo4i223908O3216xi4UdUcojxK2B0LwNwJwxyo566k1FwgU4q3G3WfKu',
#     '__csr': 'g4nb2k5Y9PgP22r3YWlTN4jRaBlEBi98ARNxcgQFdhcxhfugyKjsAOSFAGHSiTh9uCCZyOemBlqnAnym9qLqDFaQmhqmvFqZkmlvBimFGyCAJ5u8F9Vp8CEy8DBGqcypuUCWWhAi44tn8QDg-nVbDV-F8DyqBDhohFeVpWxWi8QmiECEnDx2WyQtAx6qaVEiz9CqmQdxehyoiWz4ahElAxiay9poWbyqxC5U9Wy458KWpUy2i4FGCGfwIyVaCzFEnwyXzU8UsAhaG2i48my8mwtEOQezax26oS8x6E769C826m788ocby8y7KEpwyAV8nyEKdgy58hz8y8wgVK6EHzovy8W6oG7o88nyaypqwHzUyh91qbFeq1wxK7o9y4ny6qEzG0LEfQ7oy3F1e5EcUjF0b8EG0W-3y4oC1jwWAz420aPzUAyxidxS3t1-ao4QgwHpog8fzvp4iao7u11wspWwSypoly8TgfUoKaQibK0oK023B7AomLQq0uG093g5W4Fk0dhweu0O811U0xy04Tppby86609-w0nwo04H6p7Ra0zbxW0aPU1R4cw2s82kw21U3Sw6Rw5Dw7Fzo2twyw4Yw19Uw0H20y80qQzo0WK0i22Ci06xogw15G0wO0lS7U095pK0gq2G0KYw0Mq1cDzagG0sG5U2OwRw15cw',
#     '__comet_req': '15',
#     'fb_dtsg': 'NAcN4xrUnRsyZIOKLXF2COq5vbJsSShp4kt6CZdfElGsezPkn1gpPZA:40:1684104116',
#     'jazoest': '25617',
#     'lsd': 'sbOKxNYQWQx10QyR1V77Fw',
#     '__aaid': '0',
#     '__spin_r': '1010026608',
#     '__spin_b': 'trunk',
#     '__spin_t': '1700823779',
#     'fb_api_caller_class': 'RelayModern',
#     'fb_api_req_friendly_name': 'CometMarketplaceSearchContentPaginationQuery',
#     'variables': '{"count":24,"cursor":"{\\"pg\\":0,\\"b2c\\":{\\"br\\":\\"\\",\\"it\\":0,\\"hmsr\\":false,\\"tbi\\":0},\\"c2c\\":{\\"br\\":\\"AbqKJY9sCiZe9FBJ88s6-ju1lJGrlcwHLUSHtZ183_7yv4hfLZcgVXD1a0gyIv10a_93UJHnZBvzSzFJ0fxEh_MA3HmzBqasD8aMn9pF4Ycy1n11Qns-kxLRuLI5Omoxvg-8pzklCmLksSPzafjzsGrxjdOh3BOEy7XDgaC3kHx6Y2KmRG9DznziYSp_HDaVSSLmcl9J3Vtjl0ATlbu1kVBWDNZm1-m_eVPnkUbQXwyQoJn-0AvRATZM8YGVgh5XREP0aTY7gFdOTh1-riPtEayHIz0O0yDOqf3Ljxp28R5gFwD7La81uQ9KoLazayfq2vZDbjIjfpmJDQ3ecLR6AMaqQVUyR6II_76N3uHt4IBPir2oCdLCGrIsFXvwIZyWsyT_I_5QxHSBbxZ7v7Suugg4lwMwi7bEGVCiXBesneG6DQAK6d1cdFonBS5hplxGxWPQ07iaDj8hVa6zAKnMyHvH4-VdL8I_weIGspZDY-B5NxLBXYg51v2sru5u3qS1pQg9Xp6lFJy_U2_IRz-BhTMux7SKJj3YLI5U8mDfT_lyQB0nElgXatwNp1OqbCLdB4I\\",\\"it\\":12,\\"rpbr\\":\\"\\",\\"rphr\\":false,\\"rmhr\\":false},\\"ads\\":{\\"items_since_last_ad\\":12,\\"items_retrieved\\":12,\\"ad_index\\":0,\\"ad_slot\\":0,\\"dynamic_gap_rule\\":0,\\"counted_organic_items\\":0,\\"average_organic_score\\":0,\\"is_dynamic_gap_rule_set\\":false,\\"first_organic_score\\":0,\\"is_dynamic_initial_gap_set\\":false,\\"iterated_organic_items\\":0,\\"top_organic_score\\":0,\\"feed_slice_number\\":0,\\"feed_retrieved_items\\":0,\\"ad_req_id\\":0,\\"refresh_ts\\":0,\\"cursor_id\\":61387,\\"mc_id\\":0,\\"ad_index_e2e\\":0,\\"seen_ads\\":{\\"ad_ids\\":[],\\"page_ids\\":[],\\"campaign_ids\\":[]},\\"has_ad_index_been_reset\\":false,\\"is_reconsideration_ads_dropped\\":false},\\"irr\\":false,\\"serp_cta\\":false,\\"rui\\":[],\\"mpid\\":[],\\"ubp\\":null,\\"ncrnd\\":0,\\"irsr\\":false}","params":{"bqf":{"callsite":"COMMERCE_MKTPLACE_WWW","query":"iphone"},"browse_request_params":{"commerce_enable_local_pickup":true,"commerce_enable_shipping":true,"commerce_search_and_rp_available":true,"commerce_search_and_rp_category_id":[],"commerce_search_and_rp_condition":null,"commerce_search_and_rp_ctime_days":null,"filter_location_latitude":45.4386,"filter_location_longitude":12.3267,"filter_price_lower_bound":0,"filter_price_upper_bound":214748364700,"filter_radius_km":402},"custom_request_params":{"browse_context":null,"contextual_filters":[],"referral_code":null,"saved_search_strid":null,"search_vertical":"C2C","seo_url":null,"surface":"SEARCH","virtual_contextual_filters":[]}},"scale":1.5}',
#     'server_timestamps': 'true',
#     'doc_id': '6775041392572981',
# }

# response = requests.post('https://www.facebook.com/api/graphql/', cookies=cookies, headers=headers, data=data)
# j = response.json()
# print(json.dumps(j, indent=4))