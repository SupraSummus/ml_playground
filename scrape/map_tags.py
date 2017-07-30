import argparse
import sys
import json

def map_tags(tags, tag_map):
	if tag_map is None:
		return tags, []

	else:
		mapped_tags = list()
		missing_tags = list()

		for tag in tags:
			if tag not in tag_map:
				missing_tags.append(tag)
			else:
				for mapped_tag in tag_map[tag]:
					if mapped_tag not in mapped_tags:
						mapped_tags.append(mapped_tag)

		return mapped_tags, missing_tags


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Map tags, tidy-up trainset, ...')
	parser.add_argument('-c', '--content-file', help='Content file path template.', type=str, default='{}.content')
	parser.add_argument('-t', '--tags-file', help='Tags file path template.', type=str, default='{}.tags')
	parser.add_argument('-i', '--input-file', help='Input file path template.', type=str, default='{}.in')
	parser.add_argument('-o', '--output-file', help='Output file path template.', type=str, default='{}.out')
	parser.add_argument('--missing-mappings', type=str, default='{}.missing_mappings')

	parser.add_argument('-s', '--min-size', help='Minimum content size in bytes.', type=int, default=256)
	parser.add_argument('--truncate', help='Truncate long content to this size (in bytes).', type=int, default=4*1024)
	parser.add_argument('-e', '--skip-empty-tags', help='Don\'t save articles without tags', type=bool, default=True)
	parser.add_argument('-m', '--tag-map', help='File containing tag mapping.', type=str, default=None)

	args = parser.parse_args()

	# load tag map file
	if args.tag_map is None:
		tag_map = None
	else:
		try:
			with open(args.tag_map) as f:
				tag_map = json.load(f)
		except FileNotFoundError:
			print('failed to load tag mapping {}'.format(args.tag_map), file=sys.stderr)
			tag_map = None

	for id_newline in sys.stdin:
		id = id_newline[:-1]

		# load content and tags
		with open(args.content_file.format(id), 'rb') as f:
			content = f.read(args.truncate)
		with open(args.tags_file.format(id), 'rt') as f:
			tags = f.read().splitlines()

		if len(content) < args.min_size:
			continue

		mapped_tags, missing_tags = map_tags(tags, tag_map)
		if len(missing_tags) != 0:
			with open(args.missing_mappings.format(id), 'wt') as f:
				for tag in missing_tags:
					f.write(tag)
					f.write('\n')

		if len(mapped_tags) == 0:
			continue

		# write input and output
		with open(args.input_file.format(id), 'wb') as f:
			f.write(content)
		with open(args.output_file.format(id), 'wt') as f:
			for tag in mapped_tags:
				f.write(tag)
				f.write('\n')

		print(id)
