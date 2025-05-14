#include <stdio.h>
#include <string.h>

// Le shellcode sera copié ici après génération
unsigned char shellcode[] = {};

int main(void) {
    printf("Taille du shellcode: %lu bytes\n", sizeof(shellcode));
    
    // Cast en fonction et exécution
    int (*ret)() = (int(*)())shellcode;
    ret();
    
    return 0;
} 