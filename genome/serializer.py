import struct

format = '!LLL'

def serialize_operation(code, arg0, arg1):
	return struct.pack(format, code, arg0, arg1)

def deserialize_operation(buff):
	return struct.unpack(format, buff)

def deserialize_operations(buff):
	return list(struct.iter_unpack(format, buff))

def deserialize_operations_from_stream(stream):
	s = struct.calcsize(format)
	while True:
		buff = stream.read(s)
		if len(buff) == 0:
			break
		if len(buff) != s:
			raise Exception()
		yield struct.unpack(format, buff)
