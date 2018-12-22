from django.forms import model_to_dict
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import *
from nltk import pos_tag
import re

from app.models import Emoji, EmojiKeyword

class Converter(object):
	def __init__(self, tweet):
		self.Sentences = sent_tokenize(tweet)
		self.stemmer = PorterStemmer()

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
		sent = self.__removeEmojis(sent)
		words = Split(sent)
		phrases = { }
		for slen in range(1, len(words)):
			for sshift in range(0, len(words) - slen):
				phrase = ' '.join(words[sshift:slen + sshift])
				if phrase in phrases:
					continue
				tag = TagOf(phrase)
				pair = self.__getEmojiRepresentation(phrase)
				if pair is None:
					singular = self.stemmer.stem(phrase)
					pair = self.__getEmojiRepresentation(singular)
					if pair is not None and pair.get("Emoji", None) is not None:
						if tag == "NNS":
							pair["Emoji"] *= 2
				phrases[phrase] = pair
		return phrases

	def __getEmojiRepresentation(self, phrase):
		phrase = phrase.lower()
		pairs = EmojiKeyword.objects.filter(Keyword = phrase).order_by('-Vote')
		pair = pairs.first()
		if pair is None:
			return None
		modeldict = model_to_dict(pair, fields = ("Id", "Keyword", "Emoji"))
		modeldict['HasAlternatives'] = len(pairs) > 1
		return modeldict

	def __replace(self, sent):
		sortedDict = DictToPair(self.__subsets(sent))
		for pair in enumerate(sortedDict):
			if pair[1].Value is None:
				continue
			sent = sent.replace(pair[1].Key, pair[1].Value["Emoji"])
		return sent

	def __removeEmojis(self, text):
		RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags = re.UNICODE)
		return RE_EMOJI.sub(r'', text)

class Pair(object):
	def __init__(self, key = "", value = ""):
		self.Key = key
		self.Value = value

	@property
	def WordCount(self):
		return len(Split(self.Key))

def DictToPair(d):
	l = [Pair(key, value) for key, value in d.items()]
	return sorted(l, key = lambda x: x.WordCount, reverse = True)

def Split(text):
	return re.split('[ \n]', text)

def TagOf(word):
	word = word.strip()
	if len(word) == 0:
		return ""
	return pos_tag([word])[0][1]
