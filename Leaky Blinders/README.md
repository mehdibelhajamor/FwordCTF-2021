# Leaky Blinders

### Description :
> Get the flag, by order of the leaky fookin blinders..  
> `nc 52.149.135.130 4869` 

### Files :  
*[leaky_blinders.py](https://github.com/MehdiBHA/FwordCTF-2021/blob/main/Leaky%20Blinders/leaky_blinders.py)*

### Solution : 
Reading the source code we will see that when we encrypt; if it prints a ciphertext this means that all bytes in ciphertext are different than the bytes in key in the same positions.  
So for each byte, by bruteforcing we can eliminate all 255 possible choices and all bytes remaining for each position are the bytes in key.  
Decrypt with the key and get the FLAG.

***solver.py*** :
```python
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
```

FLAG : **FwordCTF{N3v3r_x0r_w1thout_r4nd0m1s1ng_th3_k3y_0r_m4yb3_s3cur3_y0ur_c0d3}**
