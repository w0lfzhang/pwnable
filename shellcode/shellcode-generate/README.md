# Steps to generate shellcode by yourself

## write your shellcode in assemble language

## nasm -f elf binsh.asm

## ld -o binsh binsh.o

## objdump -d -F binsh

## od -A x -t x1 binsh

## copy the shellcode to hexadd0x.py to add '\x'
