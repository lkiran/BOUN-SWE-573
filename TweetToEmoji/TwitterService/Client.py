import json

from TwitterService.Authentication import Authentication

class TwitterClient(object):
	__authService = Authentication.getInstance()

	def __init__(self):
		self.__client = self.__authService.GetClient()
		self.BaseUrl = 'https://api.twitter.com/1.1/'

	def Get(self, url):
		resp, content = self.__client.request(self.BaseUrl + url, method = "GET", body = b"", headers = None)
		return json.loads(content)

	def Post(self, url, data):
		pass
