import pytz
from requests import Session
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from datetime import datetime, timedelta
from bs4 import BeautifulSoup as bs
import json
import threading as t

from timers import test_func

WEB_URL = 'https://www.dream-bid.com/auctions?locale=en'

class Bidder():

    def __init__(self):
        self.timer_number = 1
        self.countdown_function_running = True
        self.session = Session()
        self.login()
        self.auction_url = self.get_auction_url()
        [self.end_time, self.auction_id, self.bearer_token] = self.get_auction_details()
        self.session.headers.update({'authorization':self.bearer_token})

        self.bid_url = f'https://9yxm7kac4b.execute-api.eu-west-1.amazonaws.com/api/bids/{self.auction_id}'
        self.update_url = f'https://www.dream-bid.com/auctions/{self.auction_id}.json?locale=en'
        print(f'{datetime.now()} - The bid url is: {self.bid_url}')
        print(f'{datetime.now()} - The update url is: {self.update_url}')

        self.extra_time = self.get_extra_time()
        self.seconds_until_end = self.time_until_auction_end()

    def login(self, email='dmcg2448@gmail.com', password='T0wn3yg0rm'):

        login_url = 'https://www.dream-bid.com/users/sign_in?locale=en'

        signin_page_resp = self.session.get(login_url)
        signin_soup = bs(signin_page_resp.content, 'html.parser')
        authenticity_token = signin_soup.form.input['value']

        payload = {
        'authenticity_token' : authenticity_token,
        'user[login]' : email,
        'user[password]' : password,
        'user[remember_me]' : '0',
        # 'user[remember_me]' : '1',
        'commit' : 'Log in'
        }

        login_response = self.session.post(login_url, data=payload)
        if login_response.status_code == 200:
            print(f'{datetime.now()} - Logged in Successfully')
        else:
            print(f'{datetime.now()} - Log in Failed')

    def get_auction_url(self):

        main_page_url = 'https://www.dream-bid.com/auctions?locale=en'

        main_page_response = self.session.get(main_page_url)
        main_page_soup = bs(main_page_response.content, 'html.parser')

        auction_url = f'https://www.dream-bid.com{main_page_soup.find(class_="row grid-auctions__container").div.a["href"]}'

        return auction_url

    def get_auction_details(self):

        auction_response = self.session.get(self.auction_url)
        auction_soup = bs(auction_response.content, 'html.parser')

        time = auction_soup.find(class_='auction-detail__expiration-date').text

        time_object = datetime.strptime(time.strip(), '%H:%M %d/%m/%Y')
        auction_id = auction_soup.find_all(class_='auction-show')[0]['data-auction-id']
        bearer_token = f'Bearer {auction_soup.find_all(class_="center-align live-auction-detail__button-container")[0].button["data-jwt"]}'

        print(f'{datetime.now()} - Auction ends at {time_object}')
        # print(f'{datetime.now()} - The auction id is: {auction_id}')
        # print(f'{datetime.now()} - The bearer token is: {bearer_token}')

        return (time_object, auction_id, bearer_token)
    
    def place_bid(self, i='NONE'):

        start_time = datetime.now()
        resp = self.session.get(self.bid_url)
        
        print(f'{datetime.now()}: Request sent at {start_time}, from timer {i} with a response status code {resp.status_code}')

        if resp.status_code != 200:
            print(f'{datetime.now()}: Error: {resp.content}')

    def final_bids(s, bid_url):

        bid_url_list = [bid_url]*200

        MAX_WORKERS = 32

        future_list = []
        
        fs = FuturesSession(session = s, max_workers = MAX_WORKERS)
        
        for url in bid_url_list:
            future = fs.get(url)
            future_list.append(future)

        for future in as_completed(future_list):
            resp = future.result()
            print(f'{datetime.now()}: Response: {resp.status_code}')
            if resp.status_code != 200:
                print(f'{datetime.now()}: Error: {resp.content}')

    def get_extra_time(self):

        resp = self.session.get(self.update_url)
        json_resopnse = json.loads(resp.content)
        
        extra_minutes = json_resopnse['max_extra_time_minutes']

        print(f'{datetime.now()} - The extra time is: {extra_minutes} minutes')

        return extra_minutes
    
    def start_final_timer(self):

        timer = t.Timer(self.seconds_until_end, self.test_func)

        timer.start()

        print(f'{datetime.now()} - The timer has been started, the function will be triggered at {datetime.now() + timedelta(seconds=self.seconds_until_end)}')

        return timer

    def time_until_auction_end(self):

        # auction_end_time = datetime.fromisoformat('2022-01-03T12:00:00.000+00:00')

        extra_time = timedelta(minutes=self.extra_time)

        extra_time_end_time = self.end_time + extra_time

        buffer_time = timedelta(seconds=0.5)

        duration = extra_time_end_time - datetime.now() - buffer_time

        duration = duration.total_seconds()

        print(f'{datetime.now()} - The auction will end at {extra_time_end_time} which is in {duration} seconds')

        return duration

    def start_interval_timer(self):

        time_remaining = self.time_until_bid_end()
        print(f'{datetime.now()} - The time remaining is: {time_remaining}')

        timer = t.Timer(time_remaining, self.place_bid, [self.timer_number])

        print(f'{datetime.now()}: Time until bid end: {time_remaining}')
        print(f'{datetime.now()}: Timer number {self.timer_number} started')

        timer.start()

        timer.timer_number = self.timer_number

        return timer

    def time_until_bid_end(self):
        created_at = self.most_recent_update_response['bids'][0]['created_at']

        timestamp = datetime.fromisoformat(created_at)

        delay = timedelta(seconds=9,milliseconds=790)

        bid_end_timestamp = timestamp + delay

        duration = bid_end_timestamp - datetime.now(tz=pytz.utc)

        return duration.total_seconds()

    def start_countdown(self):
        print(f'{datetime.now()} - Countdown function initialized')

        update_url_list = [self.update_url]*1000000

        MAX_WORKERS = 8

        future_list = []
        

        fs = FuturesSession(max_workers = MAX_WORKERS)
        
        for url in update_url_list:
            future = fs.get(url, timeout=2)
            future_list.append(future)

        resp = self.session.get(url)
        self.most_recent_update_response = json.loads(resp.content)

        print(f'{datetime.now()} - Countdown function started')

        self.interval_timer = self.start_interval_timer()
        self.interval_timer.timer_number = self.timer_number
        current_winner = self.most_recent_update_response['bids'][0]['user']['username']
        current_winning_bid_time = datetime.fromisoformat(self.most_recent_update_response['bids'][0]['created_at'])

        print(f'{datetime.now()} - The current winning bid is {current_winner} at {current_winning_bid_time}')

        
        for future in as_completed(future_list):

            response = future.result()  
            self.most_recent_update_response = json.loads(response.content)
            
            if current_winning_bid_time < datetime.fromisoformat(self.most_recent_update_response['bids'][0]['created_at']):
                
                self.interval_timer.cancel()
                print(f'{datetime.now()} - Cancellling timer number {self.interval_timer.timer_number}')

                self.interval_timer = self.start_interval_timer()
                
                time_since_last_bid = (datetime.fromisoformat(self.most_recent_update_response['bids'][0]['created_at']) - current_winning_bid_time).total_seconds()
                current_winner = self.most_recent_update_response['bids'][0]['user']['username']
                current_winning_bid_time = datetime.fromisoformat(self.most_recent_update_response['bids'][0]['created_at'])

                print(f'{datetime.now()}: The current winning bid is {current_winner} at {current_winning_bid_time}. {time_since_last_bid} seconds since last bid')
                self.timer_number = self.timer_number + 1




    def stop_countdown(self):
        self.countdown_function_running = False
        self.interval_timer.cancel()
        print(f'{datetime.now()} - Cancellling timer number {self.interval_timer.timer_number}')
        print(f'{datetime.now()} - Stopping countdown function')

    def test_func(self,i='NONE'):
        print(f'{datetime.now()} - Test function has been triggered from timer {i}')