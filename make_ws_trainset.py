import argparse
import random
import os
import re
import subprocess


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate trainset from wikislownik.')
	parser.add_argument('-s', '--size', help='Size of generated trainset.', type=int, default=1024)
	parser.add_argument('-o', '--output', help='Output directory.', type=str, default='trainset')
	parser.add_argument('-i', '--input', help='Input directory (wikislownik).', type=str, default='wikislownik')

	args = parser.parse_args()

	i = 0
	files = os.listdir(args.input)
	random.shuffle(files)
	for filename in files:
		match = re.match('^Pl-([^\.]*).[^\.]*$', filename)
		if match:
			outdir = os.path.join(args.output, 'ws-{}'.format(filename))
			os.mkdir(outdir)

			text = match.group(1).replace('_', ' ')
			text = re.sub('-\d+$|\(\d+\)$', '', text)

			with open(os.path.join(outdir, 'out'), 'wt') as f:
				f.write(text)
				f.write('\n')

			subprocess.run([
				'sox',
				os.path.join(args.input, filename),
				'-t', 'raw',
				'-e', 'unsigned',
				'-r', '8k',
				'-b', '32',
				#'--endian', 'big',
				os.path.join(outdir, 'in'),
			])

			i += 1

		if i >= args.size:
			break
