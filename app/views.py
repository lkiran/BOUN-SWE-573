import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Processor.Converter import Converter
from TweetToEmoji.TwitterService import Client
from app.models import Emoji, EmojiKeyword

def Index(request):
	return HttpResponse(render(request, 'app/index.html'))

def GetTweets(request, q):
	client = Client.TwitterClient()
	content = client.Get('search/tweets.json', lang = 'en', q = q, result_type = 'popular', tweet_mode = 'extended')
	return HttpResponse(json.dumps(content), content_type = "application/json")

def ConvertTweet(request, tweetId):
	client = Client.TwitterClient()
	tweet = client.Get('statuses/show.json', id = tweetId, tweet_mode = 'extended')
	text = tweet.get('full_text')
	converter = Converter(text)
	result = converter.Result
	return HttpResponse(json.dumps(result), content_type = "application/json")

def GetEmojis(request, q = None):
	if q is not None:
		emojis = Emoji.objects.filter(Name__contains = q)
	else:
		emojis = Emoji.objects.all()
	ej = serializers.serialize("json", emojis)
	return HttpResponse(ej, content_type = "application/json")

@csrf_exempt
def Suggest(request):
	data = request.POST
	model = EmojiKeyword()
	model.Keyword= data['txt-phrase']
	model.Emoji = data['txt-emojis']
	model.SuggestedByUser = True
	model.save()
	if model.Id is None:
		return JsonResponse({ 'Id': None }, status = 500)
	return JsonResponse({ 'Id': model.Id}, status = 200)
