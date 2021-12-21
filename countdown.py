import requests as req
from bid import place_bid
import time as t
import json
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

def start_countdown(s, auction_id, bearer_token):

    time_url = f'https://www.dream-bid.com/auctions/{auction_id}.json?locale=en'

    s.headers.update({'authorization':bearer_token})
    bid_url = f'https://9yxm7kac4b.execute-api.eu-west-1.amazonaws.com/api/bids/{auction_id}'   

    while True:
        response = s.get(time_url)
        json_response = json.loads(response.content)
        time_remaining = json_response['time_remaining']
        print(time_remaining)
        if time_remaining <= 0.40:
            place_bid(s,bid_url)


def start_test_countdown(s, auction_id, bearer_token):
    
    time_url_list = [f'https://www.dream-bid.com/auctions/{auction_id}.json?locale=en']*100

    future_list = []

    s.headers.update({'authorization':bearer_token})
    bid_url = f'https://9yxm7kac4b.execute-api.eu-west-1.amazonaws.com/api/bids/{auction_id}'   

    fs = FuturesSession(session = s, max_workers = 16)
    j=0
    for i, url in enumerate(time_url_list):
        future = fs.get(url)
        future.i = i
        future_list.append(future)


    for future in as_completed(future_list):
        print(j)
        response = future.result()
        json_response = json.loads(response.content)
        time_remaining = json_response['time_remaining']
        if time_remaining < 0.35:
            place_bid(s,bid_url)
            print(time_remaining)
            # implement logic that check if order is correct. Then store value if less than previously stored value, else start a timer with current value
        # if j % 100 == 0:
        #     print(j)
        #     print(time_remaining)
        j=j+1