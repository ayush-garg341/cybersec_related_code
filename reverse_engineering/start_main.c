#include<stdio.h>
#include<stdlib.h>

int __libc_start_main(
    int *(main) (int, char * *, char * *),
    int argc,
    char * * ubp_av,
    void (*init) (void),
    void (*fini) (void),
    void (*rtld_fini)
    (void), void (* stack_end)
) {
    puts("Hello!");
    exit(*main(argc, ubp_av, 0));
}

// compile: gcc -shared -o start_main.so start_main.c
// LD_PRELOAD=./start_main.so ./cat cat.c
