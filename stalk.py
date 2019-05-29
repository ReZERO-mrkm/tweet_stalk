from requests_oauthlib import OAuth1Session
import json
from urllib import request
import config
from time import sleep
import requests
import traceback
import sys

keys = {
    "CK": config.api_key,
    "CS": config.api_secret,
    "AT": config.access_token,
    "AS": config.access_secret
}

sess = OAuth1Session(keys["CK"], keys["CS"], keys["AT"], keys["AS"])
TL = "https://api.twitter.com/1.1/statuses/user_timeline.json"
userIDs = config.user_ids
discord_webhook_url = config.discord_url


tmps = dict()
firsts = dict()
line = "-" * 30
for i in userIDs:
    firsts[i] = 0
while True:
    for i in userIDs:
        print(f'Processing {i} tweet')
        params1 = {
            "screen_name": i,
            "count": 1,
            "include_entities": True,
            "exclude_replies": False,
            "include_rts": True
        }
        try:
            if firsts[i] == 0:
                req = sess.get(TL, params=params1)
                timeline = json.loads(req.text)
                twi = timeline[0]
                firsts[i] += 1
                print(f'First Sending {twi["user"]["name"]} tweet.')
                payload = {'content': twi['user']['name']+ 'のつぶやき：' + twi['text']}
                requests.post(discord_webhook_url, data=payload)
                sleep(1)
                payload = {'content': line}
                requests.post(discord_webhook_url, data=payload)
                firsts[i] += 1
            elif firsts[i] == 2:
                req = sess.get(TL, params=params1)
                timeline = json.loads(req.text)
                twi = timeline[0]
                tmps[i] = twi
                firsts[i] += 1
            elif firsts[i] == 3:
                req = sess.get(TL, params=params1)
                timeline = json.loads(req.text)
                twi = timeline[0]
                if (tmps[i] != twi):
                    print(f'Sending {twi["user"]["name"]} tweet.')
                    payload = {'content': twi['user']['name'] + 'のつぶやき：' + twi['text']}
                    requests.post(discord_webhook_url, data=payload)
                    sleep(1)
                    payload = {'content': line}
                    requests.post(discord_webhook_url, data=payload)
                    firsts[i] -= 1
        except KeyboardInterrupt:
            sys.exit()
        except:
            traceback.print_exc()
        finally:
            sleep(5)
    
