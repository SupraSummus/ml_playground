from enum import Enum
from argparse import Namespace

class Operation(Enum):
	noop = Namespace(code=0)
	const = Namespace(code=1)
	deref = Namespace(code=2)

	inc = Namespace(code=10)
	dec = Namespace(code=11)
	inc_guard = Namespace(code=12)
	dec_guard = Namespace(code=13)

	mul = Namespace(code=20)
	div = Namespace(code=21)
	mod = Namespace(code=22)
