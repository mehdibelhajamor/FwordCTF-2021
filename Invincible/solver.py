from pwn import *
from Crypto.Util.number import inverse
from Crypto.Cipher import AES
from collections import namedtuple

Point = namedtuple("Point","x y")
INF = Point(0, 0)

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -0x3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b

P = Point(89995002874197087156160429731648695860910221822426040658975619972952380673767, 101442345749797973087567911870369208228023400114057003174595439233607451145078)

def add(P, Q):
	if P == INF:
		return Q
	elif Q == INF:
		return P

	if P.x == Q.x and P.y == (-Q.y % p):
		return INF
	if P != Q:
		tmp = (Q.y - P.y)*inverse(Q.x - P.x, p) % p
	else:
		tmp = (3*P.x**2 + a)*inverse(2*P.y, p) % p
	Rx = (tmp**2 - P.x - Q.x) % p
	Ry = (tmp * (P.x - Rx) - P.y) % p
	return Point(Rx, Ry)
        
def multiply(P, n):
	R = INF
	while 0 < n:
		if n & 1 == 1:
			R = add(R, P)
		n, P = n >> 1, add(P, P)
	return R

def decrypt(cipher, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    msg = aes.decrypt(cipher)
    return msg


conn = remote("52.149.135.130", 4874)
conn.recvuntil("Point x : ")
conn.sendline(str(P.x))
conn.recvuntil("Point y : ")
conn.sendline(str(P.y))
conn.recvuntil("My point : ")

Q = conn.recvline().strip().decode()[1:-1].split(',')
Q = Point(int(Q[0]), int(Q[1]))

seed = 89995002874197087156160429731648695860910221822426040658975619972952380673767
for _ in range(100):
	conn.recvuntil("Ciphertext : ")
	cipher = bytes.fromhex(conn.recvline().strip().decode())
	s = multiply(P, seed).x
	seed = s
	r = multiply(Q, s).x
	k = r & ((1<<128) - 1)
	key = hashlib.sha1(str(k).encode()).digest()[:16]
	iv = cipher[:16]
	msg = decrypt(cipher[16:], key, iv)
	conn.sendline(msg.hex())
	print(conn.recvline())
print(conn.recvline())