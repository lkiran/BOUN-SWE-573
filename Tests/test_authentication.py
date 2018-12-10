from django.test import TestCase

class TestAuthentication(TestCase):
	def test_getInstance(self):
		from TweetToEmoji.TwitterService.Authentication import Authentication
		self.assertIsNotNone(Authentication.getInstance(), "Can't get an Authentication instance")

	def test_configFileExist(self):
		from TweetToEmoji.TwitterService.Authentication import Authentication
		auth = Authentication.getInstance()
		with  open(auth.ConfigFile, 'r') as f:
			json_data = f.read()
		self.assertGreater(len(json_data), 0, "Can't read config.json")

	def test_twitterAuthentication(self):
		from oauth2 import Client
		from TweetToEmoji.TwitterService.Authentication import Authentication
		auth = Authentication.getInstance()
		client = auth.GetClient()
		self.assertEqual(type(client), Client, "Authentication client is not valid")