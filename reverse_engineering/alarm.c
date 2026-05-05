#include<stdio.h>
#include<signal.h>
#include<stdlib.h>
#include<unistd.h>

int handler(int signal)
{
    puts("DING!");
    exit(1);
}

int main() {
    alarm(3);
    signal(14, handler);
    while(1);
}

// alarm sets the timer for 3 seconds and after that it receives the signal number 14.
// Some syscalls are interrupted by the alarm (like sleep) and some are not interrupted (like read)
// On interruption, the program exits
