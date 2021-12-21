import threading as t
import time
import requests as req
import json as j
from bid import place_bid

def start_final_timer(s, bid_url, response):
    json = j.loads(response.content)
    extra_time_remaining = json['extra_time_remaining']

    timer = t.Timer(extra_time_remaining-0.5, place_bid, [s, bid_url])

    timer.start()

    return timer

def start_interval_timer(s, bid_url, time):

    timer = t.Timer(time-0.35, place_bid, [s, bid_url])

    timer.start()

    return timer