#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main()
{
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
	char s[64];
	memset(s, 0, 64);
	puts("Welcome to blind pwn!");

	while( 1)
	{
		read(0, s, 63);
		printf(s);
	}
	return 0;
}
