from django.test import TestCase

class TestTwitterClient(TestCase):
	def test_getInstance(self):
		from TweetToEmoji.TwitterService import Client
		self.assertIsNotNone(Client.TwitterClient(), "Can't get a Twitter Client instance")

	def test_get(self):
		from TweetToEmoji.TwitterService import Client
		client = Client.TwitterClient()
		content = client.Get('search/tweets.json', lang = 'en', q = 'nasa', result_type = 'popular', tweet_mode = 'extended')
		self.assertIsNone(content.get('errors'), "Can't get something from Twitter")