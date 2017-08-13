from enum import Enum
from argparse import Namespace
import random


class Operation(Enum):
	noop = Namespace(code=0)
	const = Namespace(code=1)
	#deref = Namespace(code=2)

	inc = Namespace(code=10)
	dec = Namespace(code=11)
	inc_guard = Namespace(code=12)
	dec_guard = Namespace(code=13)

	mul = Namespace(code=20)
	div = Namespace(code=21)
	mod = Namespace(code=22)

	b_not = Namespace(code=30)
	b_or = Namespace(code=31)
	b_and = Namespace(code=32)
	b_xor = Namespace(code=33)
	#b_shift = Namespace(code=34)


def random_operation(max_arg_value):
	op = random.choice(list(Operation)).value
	return (
		op.code,
		random.randrange(max_arg_value),
		random.randrange(max_arg_value),
	)
