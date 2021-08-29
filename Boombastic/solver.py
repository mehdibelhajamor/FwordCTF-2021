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