from lxml import html
import requests
import datetime
import argparse
import sys


def get_page(url):
	page = requests.get(url)
	return html.fromstring(page.content)


def get_articles(archive):
	page = get_page(archive)
	return page.xpath('//article')


def get_title(article):
	return article.attrib['data-title']


def get_id(article):
	return int(article.attrib['data-postid'])


def get_date(article):
	datetime_str = article.xpath('header//@datetime')[0]
	return datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S+00:00')


def get_content(article):
	return '\n'.join(article.xpath('div/p/text()'))


def get_tags(article):
	return article.xpath('footer//*[@rel="tag"]/text()')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Make trainset from <name>.blog.onet.pl archive posts.')
	parser.add_argument('-c', '--content-file', help='Post content file path template.', type=str, default='trainset/{}.in')
	parser.add_argument('-t', '--tags-file', help='Post tags file path template.', type=str, default='trainset/{}.out')
	parser.add_argument('url', help='Archive URL to read form (eg. \'http://nadblog-wszystkich-blogow.blog.onet.pl/2013/07/\').',)

	args = parser.parse_args()

	for article in get_articles(args.url):
		print('{}: {}'.format(get_id(article), get_title(article)), file=sys.stderr)

		with open(args.content_file.format(get_id(article)), 'w') as f:
			f.write(''.join([
				get_title(article),
				'\n',
				get_content(article),
			]))

		with open(args.tags_file.format(get_id(article)), 'w') as f:
			for tag in get_tags(article):
				f.write(tag)
				f.write('\n')
