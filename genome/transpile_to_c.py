import argparse
import struct
import sys

from serializer import deserialize_operations_from_stream
from operations import Operation

header = \
"""
#include <unistd.h>
#include <stdlib.h>

#define DATA_SIZE %d
unsigned long data[DATA_SIZE];

#define INPUT_CHUNK_SIZE %d
#define OUTPUT_CHUNK_SIZE %d


static inline unsigned long get (unsigned long loc) {
	if (loc >= DATA_SIZE) return 0;
	return data[loc];
}

static inline void set(unsigned long loc, unsigned long val) {
	if (loc >= DATA_SIZE) return;
	data[loc] = val;
}

static inline void deref(unsigned long arg0, unsigned long arg1) {
	set(arg0, get(get(arg1)));
}

static inline void inc(unsigned long arg0, unsigned long arg1) {
	set(arg0, get(arg0) + get(arg1));
}

static inline void dec(unsigned long arg0, unsigned long arg1) {
	set(arg0, get(arg0) - get(arg1));
}

static inline void mul(unsigned long arg0, unsigned long arg1) {
	set(arg0, get(arg0) * get(arg1));
}

static inline void op_div(unsigned long arg0, unsigned long arg1) {
	unsigned long v1 = get(arg1);
	if (v1 == 0) {
		set(arg0, 0);
	} else {
		set(arg0, get(arg0) / v1);
	}
}

static inline void mod(unsigned long arg0, unsigned long arg1) {
	unsigned long v1 = get(arg1);
	if (v1 <= 1) {
		set(arg0, 0);
	} else {
		set(arg0, get(arg0) %% v1);
	}
}


void read_chunk() {
	size_t offset = 0;
	while (offset < sizeof(unsigned long) * INPUT_CHUNK_SIZE) {
		ssize_t ret = read(STDIN_FILENO, (void *)data + offset, sizeof(unsigned long) * INPUT_CHUNK_SIZE - offset);
		if (ret == 0) exit(EXIT_SUCCESS);
		if (ret < 0) exit(EXIT_FAILURE);
		offset += ret;
	}
}


void write_chunk() {
	ssize_t ret = write(STDOUT_FILENO, data, sizeof(unsigned long) * OUTPUT_CHUNK_SIZE);
	if (ret != sizeof(unsigned long) * OUTPUT_CHUNK_SIZE) exit(EXIT_FAILURE);
}


void compute () {
"""

footer = \
"""
}

void main () {
	while (1) {
		read_chunk();
		compute();
		write_chunk();
	}
}
"""

c_operations = {
	Operation.noop.value.code: '/* noop {} {} */\n',
	Operation.const.value.code: 'set({}, {});\n',
	Operation.deref.value.code: 'deref({}, {});\n',

	Operation.inc.value.code: 'inc({}, {});\n',
	Operation.dec.value.code: 'dec({}, {});\n',
	#Operation.inc_guard.value.code: 'inc_guard({}, {});\n',
	#Operation.dec_guard.value.code: 'dec_guard({}, {});\n',

	Operation.mul.value.code: 'mul({}, {});\n',
	Operation.div.value.code: 'op_div({}, {});\n',
	Operation.mod.value.code: 'mod({}, {});\n',
}


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate C code based on binary genome.')
	parser.add_argument('-i', '--input', help='Binary genome file.', type=argparse.FileType('br'), default=sys.stdin.buffer)
	parser.add_argument('-o', '--output', help='File to write generated C code to.', type=argparse.FileType('tw'), default=sys.stdout)
	parser.add_argument('--memory-size', help='Operational memory size (in \'units\' - each is 4 bytes).', type=int, default=8*1024)
	parser.add_argument('--input-chunk', help='Size of input chunk in units.', type=int, default=128)
	parser.add_argument('--output-chunk', help='Size of output chunk in units.', type=int, default=4)

	args = parser.parse_args()

	args.output.write(header % (args.memory_size, args.input_chunk, args.output_chunk))
	for (code, arg0, arg1) in deserialize_operations_from_stream(args.input):
		args.output.write(c_operations.get(code, '/* unknown {} {} {} */\n'.format(code, '{}', '{}')).format(arg0, arg1))
	args.output.write(footer)
