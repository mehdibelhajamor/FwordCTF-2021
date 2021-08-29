# Procyon

### Description :
> Get Bob's trust. Or maybe try something else ?    
> `nc 52.149.135.130 4873` 

### Files :  
*[procyon.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Procyon/procyon.py)*  

### Solution : 
I'm not going through an explanation, you can read this [Paper](https://link.springer.com/content/pdf/10.1007%2F3-540-68697-5_11.pdf) it describes the original problem.  
And you can also take a look at [Raccoon Attack](https://raccoon-attack.com/)

***Solver :***
```python
from Crypto.Util.number import long_to_bytes, inverse
from sage.all import *
from pwn import *
from json import dumps, loads
from time import time
from sage.modules.free_module_integer import IntegerLattice
import random

def Prepare_matrix(vector):
    M = matrix(QQ, n+1, n+1)
    M.set_block(0, 0, p * matrix.identity(n))
    M.set_block(n, 0, matrix(QQ, 1, n+1, vector + [QQ(1)/QQ(p)]))
    return M

def Babai_CVP(lattice, vector):
    # Returns an approximate CVP solution using Babai's nearest plane algorithm.
    L = lattice.LLL()
    G, _ = L.gram_schmidt()
    diff = vector
    for i in reversed(range(L.nrows())):
        diff -=  L[i] * ((diff * G[i]) / (G[i] * G[i])).round()
    return (vector - diff).coefficients()

conn = remote("52.149.135.130", 4873)

conn.recvuntil("Alice sends to Bob : ")
Alice_params = loads(conn.recvline())
conn.recvuntil("Bob sends to Alice : ")
Bob_params = loads(conn.recvline())

t = int(time())
p = int(Alice_params['p'], 16)
g = 3
A = int(Alice_params['A'], 16)
B = int(Bob_params['B'], 16)
n = 64

conn.recvuntil("Intercepted message : ")
intercepted_msg = int(conn.recvline().strip().decode(), 16)

random_scalar = []
msb_leaked = []
for i in range(n):
    s = random.randrange(2, (p - 1) // 2)
    Y = (pow(g, s, p) * A) % p
    random_scalar.append(pow(B, s, p))
    conn.recvuntil("Send your parameters to Bob : ")
    attacker_params = {"g": hex(g), "pub": hex(Y), "p": hex(p)}
    conn.sendline(dumps(attacker_params))
    tt = int(time())
    conn.recvuntil("\nIntercepted message : ")
    leaked_data = ((int(conn.recvline().strip().decode(), 16)//tt) >> 1000) << 1000 % p
    msb_leaked.append(leaked_data)

L = Prepare_matrix(random_scalar)
u = vector(QQ, msb_leaked + [0])
v = Babai_CVP(L, u)
shared_secret = (v[-1] * p) % p
flag = (intercepted_msg - t*shared_secret) * inverse(shared_secret, p) % p
print(long_to_bytes(flag))
```

FLAG : **FwordCTF{Th3_h1dd3n_numb3r_pr0bl3m_c4nt_st4nd_4g41nst_l4tt1c3}**
