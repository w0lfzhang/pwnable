#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main()
{
  char *b = malloc(0x100);
  char *a = malloc(0x100000);
  printf("address: %p\n", a);
  read(0, a, 0x111111);
  return 0;
}
