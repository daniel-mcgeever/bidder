import requests as req
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode as encode
from login import login
from bid import place_bid
from countdown import start_countdown
from countdown import start_test_countdown
import json
import time

auction_url = 'https://www.dream-bid.com/auctions/apple-box-261221?locale=en'

s = login('dmcg2448@gmail.com', 'T0wn3yg0rm')

bid_page_response = s.get(auction_url)
bid_page_soup = bs(bid_page_response.content, 'html.parser')
auction_id = bid_page_soup.find_all(class_='auction-show')[0]['data-auction-id']
bearer_token = f'Bearer {bid_page_soup.find_all(class_="center-align live-auction-detail__button-container")[0].button["data-jwt"]}'

start_test_countdown(s,auction_id,bearer_token)