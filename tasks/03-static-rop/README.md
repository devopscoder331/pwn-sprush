title: static rop
value: 250
description: `nc pwn.sprush.rocks 33072`

### Compiling

В таске нужно отключать PIE:

```
gcc main.c -o main -no-pie
```
