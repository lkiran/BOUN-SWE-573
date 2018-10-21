from bs4 import BeautifulSoup as Soup
from urllib.request import Request, urlopen

class PageSelector(object):
	def Select(self,url, selector):
		req = Request(url, headers = { 'User-Agent': 'Chrome/60' })
		page = urlopen(req).read()
		soup = Soup(page, 'html.parser')
		return soup.select(selector)