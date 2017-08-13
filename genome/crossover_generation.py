import argparse
import random

from pool import load_genome, list_genome_names, store_genome


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Make love not war <3.')
	parser.add_argument('--pool', help='Genome pool.', type=str, default='pool')
	parser.add_argument('--count', help='Number of generated creatures.', type=int, default=8)

	args = parser.parse_args()

	for j in range(args.count):

		parent_a, parent_b = map(
			lambda name: load_genome(args.pool, name),
			random.sample(list_genome_names(args.pool), 2)
		)

		genome_len = len(parent_a)
		assert(len(parent_b) == genome_len)
		cut_point = random.randint(1, genome_len - 1)

		child = parent_a[:cut_point] + parent_b[cut_point:]
		child_name = store_genome(args.pool, child)
		print(child_name)
