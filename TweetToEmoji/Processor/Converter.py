from django.forms import model_to_dict
from nltk.tokenize import sent_tokenize
from difflib import SequenceMatcher

from app.models import Emoji, IgnoredPhrases, EmojiKeyword

class Converter(object):
	def __init__(self, tweet):
		self.Sentences = sent_tokenize(tweet)

	@property
	def Result(self):
		result = []
		for sent in self.Sentences:
			sentence_result = {
				"sentence": sent,
				"phrases": self.__subsets(sent),
				"result": self.__replace(sent)
			}
			result.append(sentence_result)
		return result

	def __subsets(self, sent):
		words = sent.split(" ")
		phrases = { }
		for slen in range(1, len(words)):
			for sshift in range(0, len(words) - slen):
				phrase = ' '.join(words[sshift:slen + sshift])
				if phrase in phrases:
					continue
				pair = self.__getEmojiRepresentation(phrase)
				phrases[phrase] = pair
		return phrases

	def __getEmojiRepresentation(self, phrase):
		pair = EmojiKeyword.objects.all().filter(Keyword = phrase).first()
		if pair is None:
			return None
		return model_to_dict(pair, fields = ("Id", "Keyword", "Emoji"))

	def __replace(self, sent):
		for phrase, emoji in self.__subsets(sent).items():
			if emoji is None:
				continue
			sent = sent.replace(phrase, emoji["Emoji"])
		return sent

def __similarityOfTwoWords(a, b):
	return SequenceMatcher(None, a, b).ratio()
