import datetime
import  requests as req
from bs4 import BeautifulSoup as bs

def place_bid(s, bid_url):

    resp = s.get(bid_url)

    print(f'{datetime.now()}: Response: {resp.status_code}')
    print(f'{datetime.now()}: Response: {resp.content}')

def final_bids(s, bid_url):

    print('test')