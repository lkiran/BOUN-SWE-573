from django.http import HttpResponse
from django.shortcuts import render

def Index(request):
	return HttpResponse(render(request,'app/index.html'))