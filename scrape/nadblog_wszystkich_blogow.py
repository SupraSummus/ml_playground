from lxml import html
import requests


main_url = 'http://nadblog-wszystkich-blogow.blog.onet.pl/'


def get_page(url):
	page = requests.get(url)
	return html.fromstring(page.content)


def get_archives():
	page = get_page(main_url)
	return page.xpath('//*[@id="archives-2"]//a/@href')


def get_articles(archive):
	page = get_page(archive)
	return page.xpath('//article')


def get_title(article):
	return article


if __name__ == '__main__':
	print(get_articles('http://nadblog-wszystkich-blogow.blog.onet.pl/2017/07/'))
