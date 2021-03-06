import argparse
import random
import tempfile
import os

from operations import Operation 
from serializer import serialize_operation


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate random generation.')
	parser.add_argument('--genome-size', help='Size of genome (operations).', type=int, default=128*1024)
	parser.add_argument('-o', '--output', help='Output directory.', type=str, default='pool')
	parser.add_argument('--max-arg-value', help='Limit generated arguments size.', type=int, default=8*1024)
	parser.add_argument('--count', help='Number of generated creatures.', type=int, default=128)

	args = parser.parse_args()

	for j in range(args.count):
		outdir = tempfile.TemporaryDirectory(
			dir=args.output,
			prefix='',
		).name
		os.mkdir(outdir)

		with open(os.path.join(outdir, 'genome'), 'wb') as f:
			for i in range(args.genome_size):
				op = random.choice(list(Operation)).value
				f.write(serialize_operation(
					op.code,
					random.randrange(args.max_arg_value),
					random.randrange(args.max_arg_value),
				))
