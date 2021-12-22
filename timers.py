import threading as t
import time
import requests as req
import json as j
from bid import place_bid, final_bids
from datetime import datetime, timezone, timedelta

def start_final_timer(s, bid_url, json):
    # json = j.loads(response.content)

    extra_time_remaining = time_until_auction_end(json)

    timer = t.Timer(extra_time_remaining, final_bids, [s, bid_url])

    timer.start()

    return timer

def start_interval_timer(s, bid_url, created_at):

    time_remaining = time_until_bid_end(created_at)

    print(time_remaining)

    timer = t.Timer(time_remaining, place_bid, [s, bid_url])

    timer.start()

    return timer



def time_until_bid_end(created_at, time_now):
    # created_at = json['bids'][0]['created_at']

    timestamp = datetime.fromisoformat(created_at)

    delay = timedelta(seconds=9,milliseconds=600)

    bid_end_timestamp = timestamp + delay
    print(bid_end_timestamp)

    duration = bid_end_timestamp - datetime.now(timezone.utc)

    return duration.total_seconds()

def time_until_auction_end(json):

    duration = json['extra_time_remaining'] - 1

    return duration