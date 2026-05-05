#include<stdio.h>
#include<signal.h>

int handler(int signal)
{
    printf("Got signal number %d!\n", signal);
}

int main(int argc, char *argv[])
{
    for(int i = 1; i <= 64; i++) signal(i, handler);
    while(1);

    return 0;
}

// gcc -o signal signal.c
// ./signal
// Try pressing Ctrl-C or Ctrl-Z and you will see the signal number.
// kill -19 $(pgrep signal) -> stop the process
// jobs
// bg -> run the process in background with signal number 18.
// fg -> run the process in foreground.
// But when you run the kill -9, that is not handled by process and the process gets killed.
// kill -9 $(pgrep signal)
// kill -l -> to list all the signals
