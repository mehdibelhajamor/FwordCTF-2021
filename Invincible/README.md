# Invincible

### Description :
> Beat me in my game, if you can.  
> `nc 52.149.135.130 4874` 

### Files :  
*[invincible.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Invincible/invincible.py)*

### Solution : 
We notice that both *Add* and *Multiply* operations are independent of `b`. Also the EllipticCurve class doesn't check for the existance of a given point.  
Since we have control on a point we can go through the Invalid Curve Attack.

By modifying `b` we can generates another curve that may have an order with a small factor.  
For exemple, `b = 3` generates a curve with order `115792089210356248762697446949407573529995394580452997270780266901612618829008` that had a small factor 3.  
So we can generate a point with order 3.  
Here's a [Sagemath](https://www.sagemath.org/) script :
```python
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -0x3
b = 3
E = EllipticCurve(GF(p), [a, b])
G = E.gens()[0]
P = G*ZZ(E.order()/3)
print(P)
```
We get this point `P = (89995002874197087156160429731648695860910221822426040658975619972952380673767, 101442345749797973087567911870369208228023400114057003174595439233607451145078)`  
It can only generates 3 point :
```
(0 : 1 : 0)
(89995002874197087156160429731648695860910221822426040658975619972952380673767 : 101442345749797973087567911870369208228023400114057003174595439233607451145078 : 1)
(89995002874197087156160429731648695860910221822426040658975619972952380673767 : 14349743460558275675129535079038365302062743301233311020938192075259646708873 : 1)
(0 : 1 : 0)
(89995002874197087156160429731648695860910221822426040658975619972952380673767 : 101442345749797973087567911870369208228023400114057003174595439233607451145078 : 1)
(89995002874197087156160429731648695860910221822426040658975619972952380673767 : 14349743460558275675129535079038365302062743301233311020938192075259646708873 : 1)
(0 : 1 : 0)
```
Choosing this point T, The first seed will always be either `0` or `89995002874197087156160429731648695860910221822426040658975619972952380673767`.  
And if we know the first seed, we can know all next seeds and so we can compute all 100 keys to decrypt each ciphertext and win the game.

***Solver :***
```python
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
```

FLAG : **FwordCTF{4lw47ys_ch3ck_1f_a_p01nt_1s_0n_th3_curv3_0r_g3t_tr1ck3d}**
