import datetime
import json

import emoji
from requests_oauthlib import OAuth1Session  # OAuthのライブラリの読み込み

import config

twitter = OAuth1Session(
    config.CONSUMER_KEY,
    config.CONSUMER_SECRET,
    config.ACCESS_TOKEN,
    config.ACCESS_TOKEN_SECRET
)

def getTweetData(search_word, until, max_id):
    url = "https://api.twitter.com/1.1/search/tweets.json"

    params = {
        'q': search_word + " -rt -bot",
        'count': '100',
        'locale': 'ja',
        'result_type': 'recent',
        'until': until,
        'include_entities': 'false',
    }

    # max_idの指定があれば設定する
    if max_id != -1:
        params['max_id'] = max_id
    # since_idの指定があれば設定する
    # if since_id != -1:
    # params['since_id'] = since_id

    req = twitter.get(url, params=params)

    if req.status_code == 200:
        timeline = json.loads(req.text)
        metadata = timeline['search_metadata']
        statuses = timeline['statuses']
        limit = req.headers['x-rate-limit-remaining'] if 'x-rate-limit-remaining' in req.headers else 0
        reset = req.headers['x-rate-limit-reset'] if 'x-rate-limit-reset' in req.headers else 0
        return {"result": True, "metadata": metadata, "statuses": statuses, "limit": limit, "reset_time": datetime.datetime.fromtimestamp(float(reset)), "reset_time_unix": reset}
    else:
        print("Error: %d" % req.status_code)
        return {"result": False, "status_code": req.status_code}


def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

