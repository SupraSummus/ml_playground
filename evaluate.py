import argparse
import subprocess
import os
import sys


# https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python_3
def longest_common_substring(s1, s2):
	m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
	longest, x_longest = 0, 0
	for x in range(1, 1 + len(s1)):
		for y in range(1, 1 + len(s2)):
			if s1[x - 1] == s2[y - 1]:
				m[x][y] = m[x - 1][y - 1] + 1
				if m[x][y] > longest:
					longest = m[x][y]
					x_longest = x
			else:
				m[x][y] = 0
	return s1[x_longest - longest: x_longest]


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Evaluate a program.')
	parser.add_argument('program', type=str)

	args = parser.parse_args()

	tests = 0
	score = 0.0
	for filename in os.listdir('trainset'):
		with open(os.path.join('trainset', filename, 'in'), 'rb') as f:
			completed = subprocess.run([args.program], input=f.read(), stdout=subprocess.PIPE)
		output = completed.stdout.decode('latin2', errors='ignore').strip().lower()
		output = output.replace('\0', '')

		with open(os.path.join('trainset', filename, 'out'), 'rt') as f:
			model = f.read().strip().lower()

		tests += 1
		score += len(longest_common_substring(output, model)) / max(len(model), len(output))

	print('{:7.5f}'.format(score/tests))
