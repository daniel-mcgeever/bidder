import requests as req
from bid import place_bid
import time as t
import json
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from timers import start_final_timer, start_interval_timer

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

    url = 'https://www.dream-bid.com/auctions/{auction_id}.json?locale=en'
    bid_url = f'https://9yxm7kac4b.execute-api.eu-west-1.amazonaws.com/api/bids/{auction_id}'  
    time_url_list = [url]*100

    resp = s.get(url)

    start_final_timer(s, bid_url, resp)

    current_winner = 'test'#json.loads(resp)['bids'][0]['id']
    
    future_list = []

    s.headers.update({'authorization':bearer_token})
     

    fs = FuturesSession(session = s, max_workers = 8)
    
    for url in time_url_list:
        future = fs.get(url)
        future_list.append(future)

    for future in as_completed(future_list):
        
        response = future.result()
        json_response = json.loads(response.content)
        time_remaining = json_response['time_remaining']
        print(f'{future.i} {time_remaining}')
        if current_winner != json_response['bids'][0]['id']:
            current_winner = json_response['bids'][0]['id']
            start_interval_timer(s, bid_url, json_response)
            print(current_winner)
        # if time_remaining < 0.35:
        #     place_bid(s,bid_url)
            
            # implement logic that check if order is correct. Then store value if less than previously stored value, else start a timer with current value
        # if j % 100 == 0:
        #     print(j)
        #     print(time_remaining)
        j=j+1