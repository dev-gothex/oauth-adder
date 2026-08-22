from curl_cffi import requests

def create_session():
    return requests.Session(impersonate="chrome145") 
