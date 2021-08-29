# Boombastic

### Description :
> A pen and a paper, thats's all you need to watch the movie.    
> `nc 52.149.135.130 4872` 

### Files :  
*[boombastic.py]()*

### Solution : 
Giving a random ticket and by doing some maths we can recover the value of `y` :

<img src="http://www.sciweavers.org/tex2img.php?eq=y%20%3D%20%28s%5E%7B2%7D%20%2B%20r%29%20%5Ctimes%20%28s%5E%7B2%7D%20-%20r%29%5E%7B-1%7D%20%20%5Cpmod%7Bp%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt="y = (s^{2} + r) \times (s^{2} - r)^{-1}  \pmod{p}" width="278" height="22" />

And so the value of `secret` :

<img src="http://www.sciweavers.org/tex2img.php?eq=secret%20%3D%20s%5E%7B-1%7D%20%5Ctimes%20%281%20%2B%20y%29%20%20%5Cpmod%7Bp%7D&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0" align="center" border="0" alt="secret = s^{-1} \times (1 + y)  \pmod{p}" width="267" height="22" />

Then, we can generate a ticket for the word "Boobmastic" and solve the challenge.

*Solver :*
```python
from Crypto.Util.number import getStrongPrime, inverse
from pwn import *
import hashlib
from json import dumps, loads

def get_ticket(code, secret, p):
    y = int(hashlib.sha256(code.encode()).hexdigest(),16)
    r = ((y**2 - 1) * (inverse(secret**2, p))) % p
    s = ((1 + y) * (inverse(secret, p))) % p
    return {'s': hex(s), 'r': hex(r), 'p': hex(p)}

conn = remote("52.149.135.130", 4872)
conn.recvuntil("> ")
conn.sendline("2")
conn.recvuntil("Your ticket : ")
ticket = loads(conn.recvline())

s = int(ticket['s'], 16)
r = int(ticket['r'], 16)
p = int(ticket['p'], 16)

a = (s**2 + r) % p
b = inverse(s**2 - r, p)
y = a*b % p

secret = inverse(s, p) * (1 + y) % p
code = "Boombastic"
magic_word = dumps(get_ticket(code, secret, p))

conn.recvuntil("> ")
conn.sendline("1")
conn.recvline("Enter the magic word : ")
conn.sendline(magic_word)
print(conn.recvline())
```

FLAG : **FwordCTF{4ct_l1k3_a_V1P_4nd_b3c0m3_a_V1P}**
