from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from ed25519 import B, l, H, Hint, mult, add, point_to_bytes, bytes_to_point
import os, hashlib, random
from pwn import *

def forge(m, pk, a):
    m = long_to_bytes(m)
    r = Hint(os.urandom(16))
    R = mult(B, r)
    S = (r + Hint(point_to_bytes(R) + pk + m) * a) % l
    return point_to_bytes(R) + long_to_bytes(S)

conn = remote("52.149.135.130", 4870)

conn.recvuntil("> ")
conn.sendline("1")

conn.recvuntil("Transfer some money to your account : ")
amount1 = 2**1034
conn.sendline(str(amount1))
s1 = bytes.fromhex(conn.recvline().strip().decode().split(' ')[-1])
pk = bytes.fromhex(conn.recvline().strip().decode().split(' ')[-1])

conn.recvuntil("> ")
conn.sendline("1")

conn.recvuntil("Transfer some money to your account : ")
amount2 = int(hashlib.sha512(long_to_bytes(amount1)).hexdigest(), 16)
conn.sendline(str(amount2))
s2 = bytes.fromhex(conn.recvline().strip().decode().split(' ')[-1])
	
R1 = bytes_to_point(s1[:32])
R2 = bytes_to_point(s2[:32])
h1 = Hint(point_to_bytes(R1) + pk + long_to_bytes(amount1))
h2 = Hint(point_to_bytes(R2) + pk + long_to_bytes(amount2))

a = (bytes_to_long(s1[32:]) - bytes_to_long(s2[32:]))*inverse(h1 - h2, l) % l

conn.recvuntil("> ")
conn.sendline("2")

amount = 2**2049
attack_sign = forge(amount, pk, a)
conn.recvuntil("\nMoney : ")
conn.sendline(str(amount))
conn.recvuntil("Code : ")
conn.sendline(attack_sign.hex())
print(conn.recvline())