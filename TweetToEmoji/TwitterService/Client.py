import json
from datetime import datetime

from TwitterService.Authentication import Authentication

class TwitterClient(object):
	__authService = Authentication.getInstance()

	def __init__(self):
		self.__client = self.__authService.GetClient()
		self.BaseUrl = 'https://api.twitter.com/1.1/'
		self.SaveToFile = True

	def GetFromHistory(self, filename):
		filename = 'TwitterService/Requests/{0}.json'.format(filename)
		json_data = open(filename).read()
		return json.loads(json_data)

	def Get(self, url, **kwargs):
		params = self.__toUrlParameter(kwargs)
		requestUrl = self.BaseUrl + url + params
		resp, content = self.__client.request(requestUrl, method = "GET", body = b"", headers = None)
		response = json.loads(content)
		response["url"] = requestUrl
		self.__saveToFile(response)
		return response

	def Post(self, url, data):
		pass

	def __toUrlParameter(self, dict):
		return "?" + '&'.join(['{0}={1}'.format(key, value) for key, value in dict.items()]) \
			if len(dict.items()) != 0 \
			else ""

	def __saveToFile(self, content):
		if self.SaveToFile:
			with open(
					'C:\\Users\\leven\\Documents\\GitHub\\BOUN-SWE-573\\TweetToEmoji\\TwitterService\\Requests\\{0}.json'.format(datetime.utcnow().strftime('%d-%m-%Y %H.%M.%S.%f')[:-3]),
					'w+') as outfile:
				json.dump(content, outfile)