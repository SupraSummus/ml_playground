import os
import tempfile
import shutil

from serializer import deserialize_operations, serialize_operation


def list_genome_names(pool):
	return os.listdir(pool)


def load_genome(pool, name):
	with open(os.path.join(pool, name, 'genome'), 'rb') as f:
		return deserialize_operations(f.read())


def store_genome(pool, genome):
	outdir = tempfile.TemporaryDirectory(
		dir=pool,
		prefix='',
	).name
	os.mkdir(outdir)

	with open(os.path.join(outdir, 'genome'), 'wb') as f:
		for op in genome:
			f.write(serialize_operation(*op))

	return os.path.basename(outdir)


def get_genome_score(pool, name):
	with open(os.path.join(pool, name, 'score'), 'rt') as f:
		return float(f.read())


def delete_genome(pool, name):
	shutil.rmtree(os.path.join(pool, name))


def move_genome(source, target, name):
	new_name = store_genome(target, load_genome(source, name))
	delete_genome(source, name)
	return new_name
