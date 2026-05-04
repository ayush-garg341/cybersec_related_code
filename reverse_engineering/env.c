#include<stdio.h>

int main(int argc, char *argv[], char *envp[]) {
    for (int i = 0; envp[i] != 0; i++)
    {
        puts(envp[i]);
    }
    return 0;
}

// Compile: gcc -o envp env.c
// ./envp
// ASDF=FDSA FOO=BAR A="B C D" ./envp
