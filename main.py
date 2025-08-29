import requests

cookies = {
    '__cf_bm': 'SIx5blX4RbWsBUQ88CDERFWcDUk9sA2YbpQnAo3fyCQ-1756394249-1.0.1.1-xIXsyhbZ8cr1WVUXF6PTn4etZzkKnRu351uw2ceCEXHwUiQuHoT5HZLhihPrGBlSsRw1hPQ_r38yByFSm7M9bC6k.O_uZd22upUb3WqeQEo',
    '_ga': 'GA1.1.2090772781.1756394250',
    '_ga': 'GA1.3.2090772781.1756394250',
    '_gid': 'GA1.3.500492869.1756394254',
    'nmstat': 'd438d7a5-d5dc-5a0b-32ba-35da19354cba',
    '_gat_UA-46452137-3': '1',
    '_ga_LV2BXW6D8Q': 'GS2.1.s1756394249$o1$g1$t1756394894$j55$l0$h0',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    # 'Cookie': '__cf_bm=SIx5blX4RbWsBUQ88CDERFWcDUk9sA2YbpQnAo3fyCQ-1756394249-1.0.1.1-xIXsyhbZ8cr1WVUXF6PTn4etZzkKnRu351uw2ceCEXHwUiQuHoT5HZLhihPrGBlSsRw1hPQ_r38yByFSm7M9bC6k.O_uZd22upUb3WqeQEo; _ga=GA1.1.2090772781.1756394250; _ga=GA1.3.2090772781.1756394250; _gid=GA1.3.500492869.1756394254; nmstat=d438d7a5-d5dc-5a0b-32ba-35da19354cba; _gat_UA-46452137-3=1; _ga_LV2BXW6D8Q=GS2.1.s1756394249$o1$g1$t1756394894$j55$l0$h0',
}

response = requests.get('https://cannabis.ny.gov/dispensary-location-verification', cookies=cookies, headers=headers)
print(response.text)