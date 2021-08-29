from Crypto.Cipher import AES
from pwn import *

conn = remote("52.149.135.130", 4869)
conn.recvuntil("Here is the encrypted flag : ")
enc_flag = bytes.fromhex(conn.recvline().strip().decode())

def xor(a, b):
    return bytearray([a[i % len(a)] ^ b[i % len(b)] for i in range(max(len(a), len(b)))])

def decrypt(cipher, k):
    aes = AES.new(k, AES.MODE_ECB)
    cipher = xor(cipher, k)
    msg = aes.decrypt(cipher)
    return msg

possible_bytes = []
for _ in range(32):
    possible_bytes.append([])
while 1:
    conn.recvuntil("> ")
    conn.sendline("1")
    cipher = conn.recvline().strip().decode()
    if cipher != "Something seems leaked !":
        cipher = bytes.fromhex(cipher)
        for i in range(len(cipher)):
            if cipher[i] not in possible_bytes[i]:
                possible_bytes[i].append(cipher[i])
        if all(len(pb) == 255 for pb in possible_bytes):
            break
key = ""
for pb in possible_bytes:
    for byte in range(256):
        if byte not in pb:
            key += chr(byte)

print(decrypt(enc_flag, key.encode('latin-1')))