# Boombastic

### Description :
> A pen and a paper, thats's all you need to watch the movie.  
> `nc 52.149.135.130 4872` 

### Files :  
*[boombastic.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Boombastic/boombastic.py)*

### Solution : 
Giving a random ticket and by doing some maths we can recover the value of `y` :

![CodeCogsEqn (3)](https://user-images.githubusercontent.com/62826765/131255494-87324103-c3de-4968-8787-8ed538bc335b.gif)

And so, the value of `secret` :

![CodeCogsEqn (5)](https://user-images.githubusercontent.com/62826765/131256289-343e1c2d-999c-474b-a7a9-53ed8d76c6ce.gif)

Then, we can generate a ticket for the word "Boobmastic" and watch the movie.

***Solver :***
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
