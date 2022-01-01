from datetime import datetime
import  requests as req
from bs4 import BeautifulSoup as bs
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed


def place_bid(s, bid_url , i):

    start_time = datetime.now()
    resp = s.get(bid_url)
    
    print(f'{datetime.now()}: Request sent at {start_time}, from timer {i} with a response status code {resp.status_code}')
    if resp.status_code != 200:
        print(f'{datetime.now()}: Error: {resp.content}')


def final_bids(s, bid_url):

    bid_url_list = [bid_url]*200

    MAX_WORKERS = 32

    future_list = []
     
    fs = FuturesSession(session = s, max_workers = MAX_WORKERS)
    
    for url in bid_url_list:
        future = fs.get(url)
        future_list.append(future)

    for future in as_completed(future_list):
        resp = future.result()
        print(f'{datetime.now()}: Response: {resp.status_code}')
        if resp.status_code != 200:
            print(f'{datetime.now()}: Error: {resp.content}')