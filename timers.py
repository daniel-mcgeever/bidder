import threading as t
import time
import requests as req
import json as j
from bid import place_bid, final_bids
from datetime import datetime, timezone, timedelta
import pytz


def start_final_timer(s, bid_url, json):
    # json = j.loads(response.content)

    extra_time_remaining = time_until_auction_end(json)

    timer = t.Timer(extra_time_remaining, final_bids, [s, bid_url])

    timer.start()

    return timer

def start_interval_timer(s, bid_url, json):

    time_remaining = time_until_bid_end(json)


    print(f'{datetime.now()}: Time until bid end: {time_remaining}')

    timer = t.Timer(10, place_bid, [s, bid_url])
    

    timer.start()
    print(f'{datetime.now()}: Timer started')


    return timer





def time_until_bid_end(json):
    created_at = json['bids'][0]['created_at']

    timestamp = datetime.fromisoformat(created_at)

    delay = timedelta(seconds=9,milliseconds=600)

    bid_end_timestamp = timestamp + delay


    duration = bid_end_timestamp - datetime.now(tz=pytz.utc)

    return duration.total_seconds()

def time_until_auction_end(json):

    duration = json['extra_time_remaining'] - 1

    return duration

def time_until_auction_start(json):

    duration = json['time_remaining']

    print(f'{datetime.now()}: Time until auction start: {duration}')

    return duration

def test_func():
    print(f'{datetime.now()}: Function triggered')