#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

char shellcode[25] = "\x6a\x0b\x58\x31\xf6\x56\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\xcd\x80";

int main(int argc, char *argv[])
{
    printf("shellcode_addr = %p\n", shellcode);
    char *buf1, *buf2, *buf3;

    if (argc != 4) 
    {
        exit(0);
    }

    buf1 = malloc(256);
    printf("buf1_addr = %p\n", buf1);
    printf("top_chunk_addr = %p\n", buf1 + 256);
    strcpy(buf1, argv[1]);
    getchar();

    printf("allocated 0x%08x bytes for buf2\n", strtoul(argv[2], NULL, 16));
    buf2 = malloc(strtoul(argv[2], NULL, 16));
    getchar();

    printf("buf2_addr = %p\n", buf2);
    buf3 = malloc(256);
    printf("buf3_addr = %p\n", buf3);
    strcpy(buf3, argv[3]);   
    
    getchar();
    read(0, buf3, 10);
    return 0;
}
//gcc -fno-stack-protector -z execstack -o force house-of-force.c
