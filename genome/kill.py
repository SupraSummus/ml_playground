import argparse
import random
from functools import lru_cache

from pool import list_genome_names, get_genome_score, move_genome


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Kill the loosers.')
	parser.add_argument('--pool', help='Genome pool.', type=str, default='pool')
	parser.add_argument('--graveyard', type=str, default='graveyard')
	parser.add_argument('--count', help='Target size of the pool.', type=int)

	args = parser.parse_args()

	@lru_cache(maxsize=None)
	def _genome_score(name):
		return get_genome_score(args.pool, name)

	genomes = sorted(list_genome_names(args.pool), key=_genome_score)

	for name in genomes[:-args.count]:
		new_name = move_genome(args.pool, args.graveyard, name)
		print(name, new_name)
