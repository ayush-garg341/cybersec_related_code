int read(int fd, char *buff, int n)
{
    buff[0] = 'p';
    buff[1] = 'w';
    buff[2] = 'n';
    buff[3] = 'e';
    buff[4] = 'd';
    buff[5] = '\n';
    return 6;
}


// Compile it as a shared library
// gcc -shared -o preload.so preload.c
