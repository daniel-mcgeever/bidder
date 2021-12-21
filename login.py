import requests as req
from bs4 import BeautifulSoup as bs
from requests.api import head

def login(email, password):

    s = req.Session()
    # headers = {
    #     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    #     'Content-Type': 'application/x-www-form-urlencoded'

    # }
    # headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    #     "Accept-Language": "en-GB,en;q=0.9",
    #     "Referer": "https://www.dream-bid.com/users/sign_in?locale=en",
    #     "Connection": "keep-alive"}
    # s.headers.update(headers)
    
    url = 'https://www.dream-bid.com/users/sign_in?locale=en'

    signin_page_resp = s.get(url)

    # s.headers.update({'Cookie':signin_page_resp.headers['Set-Cookie']})
    signin_soup = bs(signin_page_resp.content, 'html.parser')

    authenticity_token = signin_soup.form.input['value']

    payload = {
        'authenticity_token' : authenticity_token,
        'user[login]' : email,
        'user[password]' : password,
        'user[remember_me]' : '0',
        'user[remember_me]' : '1',
        'commit' : 'Log in'
    }

    

    resp = s.post(url, data=payload)

    return s