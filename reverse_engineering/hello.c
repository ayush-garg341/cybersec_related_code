#include<stdio.h>

void say_hello(char *name)
{
    printf("Hello %s!", name);
}

int main() {
    // this is the variable to hold my name
    char my_name[1024];
    scanf("%1000s", my_name);
    say_hello(my_name);
}

// gcc -o hello hello.c -> final executable.
// gcc -E hello.c -> -E preprocessor flag, that handles macro expansion, include statements, remove comments.
// In this pre-processing step, the comments are gone
// use -o option to redirect output into a file.
// gcc -E hello.c -o hello-preprocessed.c
// gcc -S -masm=intel hello-preprocessed.c -> to get the assembly of preprocessed file. It will generate a .s extension file.
// In this assembly step, the variable name is gone, it is just now a memory reference somewhere on the stack. We also lost the type information.
// If we finished compiling it like: gcc -o hello hello-preprocessed.s, we will see that some function name is also preserved.
// objdump -M intel -d hello | grep say_hello
// But this is not how a software is shipped, software is also stripped of any un-necessary metadata, to reduce the size.
// Let's verify it:
// du -sk hello
// strip hello
// du -sk hello
// We can also check string in executables like shown below:
// strings hello | grep say_hello
//
//
// We can preserve all the symbols in the binary with -g option.
// gcc -g -o hello hello.c
