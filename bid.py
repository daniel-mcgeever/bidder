from datetime import datetime
import  requests as req
from bs4 import BeautifulSoup as bs
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed


def place_bid(s, bid_url):

    resp = s.get(bid_url)

    print(f'{datetime.now()}: Response: {resp.status_code}')
    print(f'{datetime.now()}: Response: {resp.content}')

def final_bids(s, bid_url):

    bid_url_list = [bid_url]*1000

    MAX_WORKERS = 16

    future_list = []
     
    fs = FuturesSession(session = s, max_workers = MAX_WORKERS)
    
    for url in bid_url_list:
        future = fs.get(url)
        future_list.append(future)

    for future in as_completed(future_list):
        print(f'{datetime.now()}: Response: {future.result().status_code}')
        print(f'{datetime.now()}: Response: {future.result().content}')