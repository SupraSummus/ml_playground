import argparse
from lxml import html
import requests
import sys


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='List URLs of <name>.blog.onet.pl archives.')
	parser.add_argument('-o', '--output', help='File to write to.', type=argparse.FileType('w'), default=sys.stdout)
	parser.add_argument('url', help='URL to exctract from (eg. \'http://nadblog-wszystkich-blogow.blog.onet.pl/\')',)

	args = parser.parse_args()

	page = html.fromstring(requests.get(args.url).content)
	archives = page.xpath('//*[@id="archives-2"]//a/@href')
	for archive in archives:
		args.output.write(archive)
		args.output.write('\n')
