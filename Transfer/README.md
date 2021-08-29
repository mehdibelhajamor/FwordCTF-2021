# Transfer

### Description :
> My friend got access to the National Bank Money Transfer. He tried to transfer money to his account as much as he wants BUT it's limited.  
> Could you break it ?  
> `nc 52.149.135.130 4870` 

### Files :  
*[transfer.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Transfer/transfer.py)*  
*[ed25519.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Transfer/ed25519.py)*

### Solution : 
[Ed25519](https://en.wikipedia.org/wiki/EdDSA) is still compromised if two different messages are signed using the same value for `r`. This is obviously impossible in theory, since it is deterministic. But what if an error occurs during the computation of `Hint(R, pk, m)` and produces a `S'` instead ?  
This can causes a Fault Attack, where we can possibly recover the value `a` by computing :

![CodeCogsEqn (2)](https://user-images.githubusercontent.com/62826765/131237348-8b95980d-1677-4616-97f9-349a85e0a901.gif)

with `h = Hint(R, pk, m)` and `h' = Hint(R', pk, m)`

Here `r` generates as follow `Hint(h[32:] + hmac.new(m, h, digestmod=hashlib.sha512).digest())` and that made it more secure since we will always get a unique value `r` for every signed message. Or is it really secure ?

Basically, There's a bug in HMAC that if the key is longer than the block size, it's hashed with the HMAC cryptographic hash, then appended with zeros to fit the single block and that causes collisions. Read more about [Breaking HMAC](https://pthree.org/2016/07/29/breaking-hmac/).

So using this property, we can break the Ed25519 using Fault Attack and transfer the money we wants.

***Solver :***
```python
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
```

FLAG : **FwordCTF{B3_a_b1t_m0r3_c4r3ful_n3xt_t1m3_p1ck1ng_y0ur_h4sh_alg0r1thm}**
