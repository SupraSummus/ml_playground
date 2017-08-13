import argparse
import random

from pool import load_genome, list_genome_names, store_genome
from operations import random_operation


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Duplicate genome fragment.')
	parser.add_argument('--pool', help='Genome pool.', type=str, default='pool')
	parser.add_argument('--count', help='Number of generated creatures.', type=int, default=8)
	parser.add_argument('--span-min', type=int)
	parser.add_argument('--span-max', type=int)

	args = parser.parse_args()

	for j in range(args.count):

		genome = load_genome(
			args.pool,
			random.choice(list_genome_names(args.pool)),
		)

		span = random.randrange(args.span_min, args.span_max)
		src_start = random.randrange(0, len(genome) - span - 1)
		dst_start = random.randrange(0, len(genome) - span - 1)
		fragment = genome[src_start:src_start + span]
		genome[dst_start:dst_start + span] = fragment

		genome_name = store_genome(args.pool, genome)
		print(genome_name)
