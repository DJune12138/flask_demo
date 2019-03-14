# -*- coding:utf-8 -*-

#########################################
#########################################
## 本模块用于解析各种erlang term表示数据
## 部分非常规类型未支持
#########################################
#########################################
#########################################

import struct

def binary_to_term(s):
	if type(s) != type(''):
		return s
	if len(s) == 0:
		return s

	(Type, ) = struct.unpack("B", s[0])
	if Type == 131:
		try:
			return binary_to_term2(s[1:])[0]
		except:
			print "exception.........."
			return s
	else:
		return s

def binary_to_term2(s):
	(Type, ) = struct.unpack("B", s[0])
	return binary_to_term_type(Type, s[1:])

def binary_to_term_type(Type, S):
	if Type == 70:
		return binary_to_term_float(S[:8]), S[8:]
	elif Type == 77:
		return "not implement",
	elif Type == 82:
		return binary_to_term_byte(S[0]), S[1:]
	elif Type == 97:
		return binary_to_term_byte(S[0]), S[1:]
	elif Type == 98:
		return binary_to_term_int(S[:4]), S[4:]
	elif Type == 99:
		return "old format float", S[31:]
	elif Type == 100:
		return binary_to_term_string(binary_to_term_ushort(S[:2]), S[2:])
	elif Type == 101:
		return "not implement",
	elif Type == 102:
		return "not implement",
	elif Type == 103:
		return "not implement",
	elif Type == 104:
		return binary_to_term_tuple(binary_to_term_byte(S[0]), S[1:])
	elif Type == 105:
		return binary_to_term_tuple(binary_to_term_uint(S[:4]), S[4:])
	elif Type == 106:
		return "[]", S
	elif Type == 107:
		return binary_to_term_string(binary_to_term_ushort(S[:2]), S[2:])
	elif Type == 108:
		return binary_to_term_list(binary_to_term_uint(S[:4]), S[4:])
	elif Type == 109:
		return binary_to_term_string(binary_to_term_uint(S[:4]), S[4:])
	elif Type == 110:
		return binary_to_term_large(binary_to_term_byte(S[0]), binary_to_term_byte(S[1]), S[2:])
	elif Type == 111:
		return binary_to_term_large(binary_to_term_uint(S[:4]), binary_to_term_byte(S[4]), S[5:])
	elif Type == 112:
		return "not implement",
	elif Type == 113:
		return "not implement",
	elif Type == 114:
		return "not implement",
	elif Type == 115:
		return binary_to_term_string(binary_to_term_byte(S[0]), S[1:])
	elif Type == 116:
		return binary_to_term_map(binary_to_term_uint(S[:4]), S[4:])
	elif Type == 117:
		return "not implement",
	elif Type == 118:
		return binary_to_term_string(binary_to_term_ushort(S[:2]), S[2:])
	elif Type == 119:
		return binary_to_term_string(binary_to_term_byte(S[0]), S[1:])
	else:
		print Type
		return "err type %s" % Type,

def binary_to_term_byte(S):
	(V, ) = struct.unpack("B", S)
	return V

def binary_to_term_int(S):
	(V, ) = struct.unpack(">i", S)
	return V

def binary_to_term_uint(S):
	(V, ) = struct.unpack(">I", S)
	return V

def binary_to_term_ushort(S):
	(V, ) = struct.unpack(">H", S)
	return V

def binary_to_term_tuple(Arity, S):
	Res = []
	for i in range(0, Arity):
		V, S = binary_to_term2(S)
		Res.append(V)

	return Res, S

def binary_to_term_map(Arity, S):
	Res = []
	for i in range(0, Arity):
		K, S = binary_to_term2(S)
		V, S = binary_to_term2(S)
		Res.append((K, V))

	return Res, S

def binary_to_term_float(S):
	(V, ) = struct.unpack(">d", S)
	return V

def binary_to_term_string(Len, S):
	return S[:Len], S[Len:]

def binary_to_term_list(Len, S):
	Res = []
	for i in range(0, Len):
		V, S = binary_to_term2(S)
		Res.append(V)

	if binary_to_term_byte(S[0]) == 106:
		return Res, S[1:]
	else:
		return Res, S

def binary_to_term_large(Len, Negative, S):
	V = 0

	for i in range(0, Len):
		E = binary_to_term_byte(S[i])
		V = V + E * (256 ** i)

	if Negative == 1:
		V = -V
		
	return V, S[Len:]

# def array_to_term(A):
# 	Res = []
# 	for i in A:
# 		Res.append(struct.pack("B", i))
# 	return "".join(Res)
