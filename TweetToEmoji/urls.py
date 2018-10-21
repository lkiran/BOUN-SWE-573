"""TweetToEmoji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
	url(r'^$', views.Index, name ='index'),
	path('admin/', admin.site.urls),
]

# client = TwitterClient()
# content = client.Get('statuses/home_timeline.json')
#
# print(content)
# ps = PageSelector()
# baseUrl = 'https://emojipedia.org'
# url = baseUrl + '/twitter/'
# selector = 'body > div.container > div.content > article > ul > li'
#
# list = ps.Select(url, selector)
# length = len(list)
# for index, item in enumerate(list):
# 	try:
# 		href = item.find('a').attrs['href']
# 		emojiPage = ps.Select(baseUrl + href, 'article')[0]
#
# 		model = Emoji()
# 		model.Icon = emojiPage.select('#emoji-copy')[0].attrs['value']
# 		model.Name = emojiPage.select('h1')[0].contents[1]
# 		model.Description = emojiPage.select('.description')[0].contents[1].text
# 		model.Order = index
#
# 		model = model.save()
# 		print('{0} of {1} - {2}'.format(index, length, model))
#
# 	except Exception as e:
# 		print(e)
