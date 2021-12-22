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

    url = f'https://www.dream-bid.com/auctions/{auction_id}.json?locale=en'
    bid_url = f'https://9yxm7kac4b.execute-api.eu-west-1.amazonaws.com/api/bids/{auction_id}'  
    time_url_list = [url]*10000
    s.headers.update({'authorization':bearer_token})


    MAX_WORKERS = 8

    
    
    future_list = []

    
     

    fs = FuturesSession(session = s, max_workers = MAX_WORKERS)
    
    for url in time_url_list:
        future = fs.get(url)
        future_list.append(future)

    # Implement a block here that starts the initial interval timer and pass reference into for loop
    resp = s.get(url)
    json_response = json.loads(resp.content)
    timer = start_interval_timer(s, bid_url, json_response)
    # final_timer = start_final_timer(s, bid_url, json_response)
    current_winner = json_response['bids'][0]['user']['username']
    j = 0
    for future in as_completed(future_list):
        if j == 0:
            response = future.result()  
            json_response = json.loads(response.content)
            
            if current_winner != json_response['bids'][0]['user']['username']:
                timer.cancel()
                current_winner = json_response['bids'][0]['user']['username']
                timer = start_interval_timer(s, bid_url, json_response)
                j = MAX_WORKERS*2
                print(f'{current_winner}')
        else:
            j = j - 1
