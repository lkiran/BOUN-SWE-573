import json

import oauth2

class Authentication(object):
	__instance = None

	@staticmethod
	def getInstance():
		""" Static access method. """
		if Authentication.__instance == None:
			Authentication()
		return Authentication.__instance

	def __init__(self):
		""" Virtually private constructor. """
		if Authentication.__instance is not None:
			raise Exception("This class is a singleton! Try 'Authentication.getInstance()'")
		else:
			self.__load()
			Authentication.__instance = self

	def __load(self):
		self.ConfigFile = 'C:\\Users\\leven\\Documents\\GitHub\\BOUN-SWE-573\\TweetToEmoji\\config.json'
		with  open(self.ConfigFile, 'r') as f:
			json_data = f.read()
		data = json.loads(json_data)
		self.API_SECRET_KEY = data.get('API_SECRET_KEY', "")
		if not self.API_SECRET_KEY:
			raise Exception("'API_SECRET_KEY' key is not found in 'config.json' or empty!")
		self.API_KEY = data.get('API_KEY', "")
		if not self.API_KEY:
			raise Exception("'API_KEY' key is not found in 'config.json' or empty!")
		self.ACCESS_TOKEN = data.get('ACCESS_TOKEN', "")
		if not self.ACCESS_TOKEN:
			raise Exception("'ACCESS_TOKEN' key is not found in 'config.json' or empty!")
		self.ACCESS_TOKEN_SECRET = data.get('ACCESS_TOKEN_SECRET', "")
		if not self.ACCESS_TOKEN_SECRET:
			raise Exception("'ACCESS_TOKEN_SECRET' key is not found in 'config.json' or empty!")

	def GetClient(self):
		consumer = oauth2.Consumer(key = self.API_KEY, secret = self.API_SECRET_KEY)
		token = oauth2.Token(key = self.ACCESS_TOKEN, secret = self.ACCESS_TOKEN_SECRET)
		client = oauth2.Client(consumer, token)
		return client
