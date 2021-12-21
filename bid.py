import  requests as req
from bs4 import BeautifulSoup as bs

def place_bid(s, bid_url):

    resp = s.get(bid_url)

    print(resp.status_code)
    print(resp.content)