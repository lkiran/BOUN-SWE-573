from nltk.tokenize import sent_tokenize
from difflib import SequenceMatcher

from app.models import Emoji, IgnoredPhrases

class Converter(object):
	def __init__(self, tweet):
		self.Text = tweet.get('text', '')
		self.Sentences = sent_tokenize(self.Text)

		print(self.Text)
		print(self.Sentences)

	@property
	def Result(self):
		for sent in self.Sentences:
			self.__subsets(sent)
		return ""

	def __subsets(self, sent):
		words = sent.split(" ")
		for slen in range(1, len(words)):
			for sshift in range(0, len(words) - slen):
				phrase = ' '.join(words[sshift:slen + sshift])
				emojiList = self.__getEmojiListOfPhrase(phrase)
				if emojiList:
					print(phrase, emojiList)

	def __getEmojiListOfPhrase(self, phrase):
		ignoredPhrase = IgnoredPhrases.objects.filter(Phrase = phrase)
		if len(ignoredPhrase):
			return None
		emojiList = Emoji.objects.filter(Description__contains = phrase)
		if len(emojiList) == 0:
			return None
		if len(emojiList) > 20:
			ignore = IgnoredPhrases()
			ignore.Phrase = phrase
			ignore.save()
			return None
		return set(emojiList)


def __similarityOfTwoWords(a, b):
	return SequenceMatcher(None, a, b).ratio()
