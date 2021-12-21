import requests as req
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from bs4 import BeautifulSoup as bs
from urllib.parse import urlencode as encode
from login import login
from bid import place_bid
from countdown import start_countdown
import json
import time
from datetime import datetime, timedelta, timezone
from timers import time_until_auction_end, time_until_bid_end



s = req.Session()

resp = s.get('https://www.dream-bid.com/auctions/050c5b8b-ba8c-4dea-b92a-f7cfc8c5a0cb.json?locale=en')

json = json.loads(resp.content)

print(time_until_auction_end(json))