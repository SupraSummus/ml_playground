import argparse
from pprint import pprint
import requests


def get_list(category, gcmcontinue=None):
	return requests.get(
		'https://commons.wikimedia.org/w/api.php',
		params={
			'format': 'json',
			'action': 'query',
			'generator': 'categorymembers',
			'gcmtitle': 'Category:{}'.format(category),
			'gcmtype': 'file',
			'gcmlimit': 500,
			'gcmcontinue': gcmcontinue,
			'prop': 'imageinfo',
			'iiprop': 'url',
		},
	).json()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Get files in category from wikimedia.')
	parser.add_argument('category', type=str)
	args = parser.parse_args()
	
	gcmcontinue = None
	while True:
		data = get_list(args.category, gcmcontinue)
		
		for member in data['query']['pages'].values():
			for l in member['imageinfo']:
				print(l['url'])
		
		gcmcontinue = data.get('continue', {}).get('gcmcontinue', None)
		if gcmcontinue is None:
			break
