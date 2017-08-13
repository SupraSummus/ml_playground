import argparse
import random

from pool import load_genome, list_genome_names, store_genome
from operations import random_operation


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Copy genomes with mutations.')
	parser.add_argument('--pool', help='Genome pool.', type=str, default='pool')
	parser.add_argument('--count', help='Number of generated creatures.', type=int, default=8)
	parser.add_argument('--span-min', type=int)
	parser.add_argument('--span-max', type=int)
	parser.add_argument('--max-arg-value', help='Limit generated arguments size.', type=int, default=8*1024)

	args = parser.parse_args()

	for j in range(args.count):

		genome = load_genome(
			args.pool,
			random.choice(list_genome_names(args.pool)),
		)

		span = random.randrange(args.span_min, args.span_max)
		start = random.randrange(0, len(genome) - span - 1)
		for i in range(start, start + span + 1):
			genome[i] = random_operation(args.max_arg_value)

		genome_name = store_genome(args.pool, genome)
		print(genome_name)
