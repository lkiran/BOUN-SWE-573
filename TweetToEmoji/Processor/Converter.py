from django.forms import model_to_dict
from nltk.tokenize import sent_tokenize
from nltk.stem.porter import *
from nltk import pos_tag

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
		words = sent.split(" ")
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
		pair = EmojiKeyword.objects.all().filter(Keyword = phrase).first()
		if pair is None:
			return None
		return model_to_dict(pair, fields = ("Id", "Keyword", "Emoji"))

	def __replace(self, sent):
		sortedDict = DictToPair(self.__subsets(sent))
		for pair in enumerate(sortedDict):
			if pair[1].Value is None:
				continue
			sent = sent.replace(pair[1].Key, pair[1].Value["Emoji"])
		return sent

class Pair(object):
	def __init__(self, key = "", value = ""):
		self.Key = key
		self.Value = value

	@property
	def WordCount(self):
		return len(self.Key.split(" "))

def DictToPair(d):
	l = [Pair(key, value) for key, value in d.items()]
	return sorted(l, key = lambda x: x.WordCount, reverse = True)

def TagOf(word):
	word = word.strip()
	if len(word) == 0:
		return ""
	return pos_tag([word])[0][1]
