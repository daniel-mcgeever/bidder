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



