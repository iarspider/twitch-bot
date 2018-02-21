#!python3
# -*- coding: utf-8 -*-
import simplejson
from requests_oauthlib import OAuth2Session


def token_saver(token):
    with open("token.json", "w") as f:
        simplejson.dump(token, f)


def get_token(client_id, client_secret, redirect_uri):
    scope = ['points.read', 'points.write']
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    authorization_url, state = oauth.authorization_url("https://streamlabs.com/api/v1.0/authorize")
    print('Please go to\n %s\n and authorize access.' % authorization_url)

    authorization_response = input('Enter the full callback URL').strip()
    token = oauth.fetch_token("https://streamlabs.com/api/v1.0/token", client_id=client_id, client_secret=client_secret,
                              authorization_response=authorization_response)

    token_saver(token)
    return token


def get_streamlabs_session(client_id, client_secret, redirect_uri):
    try:
        f = open("token.json", 'r')
        token = simplejson.load(f)
    except (OSError, simplejson.JSONDecodeError):
        print("Failed to load token!")
        token = get_token(client_id, client_secret, redirect_uri)

    scope = ['points.read', 'points.write']
    oauth = OAuth2Session(client_id, token=token, auto_refresh_url="https://streamlabs.com/api/v1.0/authorize",
                          redirect_uri=redirect_uri, scope=scope)

    return oauth


def get_points(oauth, username, channel='iarspider'):
    r = oauth.get('https://streamlabs.com/api/v1.0/points', params=dict(username=username, channel=channel))
    r.raise_for_status()
    return r.json()


def sub_points(oauth, username, points, channel='iarspider'):
    r = oauth.post('https://streamlabs.com/api/v1.0/points/subtract',
                   data=dict(username=username, channel=channel, points=points))
    r.raise_for_status()
    return r.json()


def main():
    from config import client_id, client_secret, redirect_uri
    import logging
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        # noinspection PyUnresolvedReferences
        import httplib as http_client

    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True
    oauth = get_streamlabs_session(client_id, client_secret, redirect_uri)
    points = get_points(oauth, 'iarspider')
    from pprint import pprint
    pprint(points)


if __name__ == "__main__":
    main()
