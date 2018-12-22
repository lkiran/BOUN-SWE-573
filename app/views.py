import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from TweetToEmoji.Processor.Converter import Converter
from TweetToEmoji.TwitterService import Client
from app.models import Emoji, EmojiKeyword

def Index(request):
	return HttpResponse(render(request, 'app/index.html'))

def GetTweets(request, q):
	client = Client.TwitterClient()
	content = { }
	if q.startswith('tweetid='):
		tweetId = q.replace('tweetid=', '')
		tweet = client.Get('statuses/show.json', id = tweetId, tweet_mode = 'extended')
		content['statuses'] = [tweet]
	else:
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

def GetOtherEmojiKeywords(request, id):
	pair = EmojiKeyword.objects.filter(Id = id).first()
	others =EmojiKeyword.objects\
		.filter(Keyword = pair.Keyword)\
		.exclude(Id = id)
	json = serializers.serialize("json", others)
	return HttpResponse(json, content_type = "application/json")

@csrf_exempt
def Vote(request):
	data = request.POST
	id = data['id']
	model = EmojiKeyword.objects.filter(Id = id).first()
	if model is None:
		raise Exception("EmojiKeyword with id={0} could not be found".format(id))
	up = bool(data['up'])
	newVote = model.Vote
	if up:
		newVote += 1
	else:
		newVote -= 1
	model.Vote = newVote
	model.save()
	if model.Vote is newVote:
		return JsonResponse({ 'Id': model.Id }, status = 200)
	return JsonResponse({ 'Id': None }, status = 500)

@csrf_exempt
def Suggest(request):
	data = request.POST
	model = EmojiKeyword()
	keywordInput = data['txt-phrase'].strip().lower()
	model.Keyword = keywordInput
	model.Emoji = data['txt-emojis']
	model.SuggestedByUser = True
	model.save()
	if model.Id is None:
		return JsonResponse({ 'Id': None }, status = 500)
	return JsonResponse({ 'Id': model.Id }, status = 200)
