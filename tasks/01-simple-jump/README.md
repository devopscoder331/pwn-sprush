# simple jump

### Descriptions

title: simple jump
value: 100
description: `nc 51.250.109.202 33069`

### Pre-paring

```
pip install --upgrade pwntools --break-system-packages
```


### Hints

```
python -c "import struct; print(struct.pack('<Q', 0x0000000000401156))"
```