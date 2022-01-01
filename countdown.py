import requests as req
from bid import place_bid
import time as t
import json
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from timers import start_final_timer, start_interval_timer
from datetime import datetime

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
    print(f'{datetime.now()}: Countdown function initialized')

    url = f'https://www.dream-bid.com/auctions/{auction_id}.json?locale=en'
    bid_url = f'https://9yxm7kac4b.execute-api.eu-west-1.amazonaws.com/api/bids/{auction_id}'  
    time_url_list = [url]*1000000
    s.headers.update({'authorization':bearer_token})

    MAX_WORKERS = 8

    future_list = []
     
    # fs = FuturesSession(session = s, max_workers = MAX_WORKERS)
    fs = FuturesSession(max_workers = MAX_WORKERS)
    
    for url in time_url_list:
        future = fs.get(url)
        future_list.append(future)

    resp = s.get(url)
    json_response = json.loads(resp.content)

    

    final_timer = start_final_timer(s, bid_url, json_response)
    timer = (start_interval_timer(s, bid_url, json_response ,0), 0)
    current_winner = json_response['bids'][0]['user']['username']
    current_winning_bid_time = datetime.fromisoformat(json_response['bids'][0]['created_at'])

    print(f'{datetime.now()}: Timer number {timer[1]} started')
    print(f'{datetime.now()}: The current winning bid is {current_winner} at {current_winning_bid_time}')

    i=1
    for future in as_completed(future_list):

        response = future.result()  
        json_response = json.loads(response.content)
        
        if current_winning_bid_time < datetime.fromisoformat(json_response['bids'][0]['created_at']):

            print(f'{datetime.now()}: Cancellling timer nnumber {timer[1]}')
            timer[0].cancel()

            time_since_last_bid = (datetime.fromisoformat(json_response['bids'][0]['created_at']) - current_winning_bid_time).total_seconds()
            current_winner = json_response['bids'][0]['user']['username']
            current_winning_bid_time = datetime.fromisoformat(json_response['bids'][0]['created_at'])

            # created_at = json_response['bids'][0]['created_at']
            # time_now = response.headers

            timer = (start_interval_timer(s, bid_url, json_response, i), i)

            print(f'{datetime.now()}: The current winning bid is {current_winner} at {current_winning_bid_time}. {time_since_last_bid} seconds since last bid')
            i=i+1




def convert_date(unparsed):
    t = datetime.strptime(unparsed, '%a, %d %b %Y %H:%M:%S %Z')
    return t