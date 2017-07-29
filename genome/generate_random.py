import argparse
import random
import sys

from operations import Operation 
from serializer import serialize_operation


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate random binary genome.')
	parser.add_argument('-s', '--size', help='Size of genome (operations).', type=int, default=128*1024)
	parser.add_argument('-o', '--output', help='File to write to.', type=argparse.FileType('bw'), default=sys.stdout.buffer)
	parser.add_argument('--max-arg-value', help='Limit generated arguments size.', type=int, default=8*1024)

	args = parser.parse_args()

	for i in range(args.size):
		op = random.choice(list(Operation)).value
		args.output.write(serialize_operation(
			op.code,
			random.randrange(args.max_arg_value),
			random.randrange(args.max_arg_value),
		))
