from datetime import datetime
import threading
import requests as req
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode as encode
from login import login
from bid import place_bid
from countdown import start_countdown
from countdown import start_test_countdown
import json
import time
from timers import time_until_auction_start

def get_end_time_from_response(response_soup):

    time = response_soup.find(class_='auction-detail__expiration-date').text

    time_object = datetime.strptime(time.strip(), '%H:%M %d/%m/%Y')

    return time_object

auction_url = 'https://www.dream-bid.com/auctions/ysl-wallet-030122?locale=en'


s = login('dmcg2448@gmail.com', 'T0wn3yg0rm')

bid_page_response = s.get(auction_url)
bid_page_soup = bs(bid_page_response.content, 'html.parser')
auction_id = bid_page_soup.find_all(class_='auction-show')[0]['data-auction-id']
bearer_token = f'Bearer {bid_page_soup.find_all(class_="center-align live-auction-detail__button-container")[0].button["data-jwt"]}'
url = f'https://www.dream-bid.com/auctions/{auction_id}.json?locale=en'

response = s.get(url)

json_response = json.loads(response.content)

# start_auction_start_timer(s, json_response, auction_id, bearer_token)

time_until_start = time_until_auction_start(json_response)

auction_end_time = get_end_time_from_response(bid_page_soup)


timer = threading.Timer(time_until_start, start_countdown, [s, auction_id, bearer_token, auction_end_time])
timer.start()



# start_test_countdown(s,auction_id,bearer_token)

