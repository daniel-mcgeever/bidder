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

    timer = t.Timer(time_remaining, place_bid, [s, bid_url])

    print(f'{datetime.now()}: Time until bid end: {time_remaining}')

    timer.start()

    return timer





def time_until_bid_end(json):
    created_at = json['bids'][0]['created_at']

    timestamp = datetime.fromisoformat(created_at)

    delay = timedelta(seconds=9,milliseconds=700)

    bid_end_timestamp = timestamp + delay


    duration = bid_end_timestamp - datetime.now(tz=pytz.utc)

    return duration.total_seconds()

def time_until_auction_end(json):

    auction_end_time = datetime.fromisoformat(json['current_end_at'])

    extra_time = timedelta(minutes=json['max_extra_time_minutes'])

    extra_time_end_time = auction_end_time + extra_time

    buffer_time = timedelta(seconds=0.3)

    duration = extra_time_end_time - datetime.now(tz=pytz.utc) - buffer_time

    return duration.total_seconds()

def time_until_auction_start(json):

    duration = json['time_remaining']

    print(f'{datetime.now()}: Time until auction start: {duration}')

    return duration

def test_func():
    print(f'{datetime.now()}: Function triggered')