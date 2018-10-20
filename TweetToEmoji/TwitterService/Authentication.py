import json

import oauth2

class Authentication(object):
	def __init__(self):
		json_data = open('config.json').read()
		data = json.loads(json_data)
		self.CONSUMER_SECRET = data.get('CONSUMER_SECRET', "")
		self.CONSUMER_KEY = data.get('CONSUMER_KEY', "")

	def oauth_req(self, url, key, secret, http_method = "GET", post_body = "", http_headers = None):
		consumer = oauth2.Consumer(key = self.CONSUMER_KEY, secret = self.CONSUMER_SECRET)
		token = oauth2.Token(key = key, secret = secret)
		client = oauth2.Client(consumer, token)
		resp, content = client.request(url, method = http_method, body = post_body, headers = http_headers)
		return content

	# home_timeline = oauth_req('https://api.twitter.com/1.1/statuses/home_timeline.json', 'abcdefg', 'hijklmnop')
