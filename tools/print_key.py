"""Simple script to print hard-coded key in the same format as output of knwown_bits.py,
allowing to compare them"""
key=[0x0f,0x1e,0x2d,0x3c,0x4b,0x5a,0x69,0x78,0x87,0x96,0xa5,0xb4,0xc3,0xd2,0xe1,0xf0]
key_bits_str = ""
for k in range(16):
    add_str = bin(key[k])[2:]
    key_bits_str += '0'*(8-len(add_str)) + add_str + ' '
print(key_bits_str)
