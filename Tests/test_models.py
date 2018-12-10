from django.test import TestCase
from app.models import Emoji
# Create your tests here.
class TestEmoji(TestCase):
	def test_getFromDatabase(self):
		emoji = Emoji.objects.all()
		self.assertGreater(len(emoji), 0, "Can't get any emoji from database")