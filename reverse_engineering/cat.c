#include<unistd.h>
#include<fcntl.h>

int main(int argc, char *argv[])
{
    char buff[1024];
    int n;

    int fd = argc == 1 ? 0 : open(argv[1], 0);

    while((n = read(fd, buff, 1024)) > 0 && write(1, buff, n) > 0);
}

// Compile it: gcc -o cat cat.c
// readelf -a /bin/cat | grep interp -> to check the interpreter
// sudo apt install patchelf
// patchelf --set-interpreter /some/interpreter ./cat
// Now executing - ./cat will give "No such file or directory" because /some/interpreter does not exist.
// readelf -a ./cat | grep interp -> it will give: [Requesting program interpreter: /some/interpreter]
// ldd ./cat -> list dynamic dependencies

// Now execute with arbitrary injected preload path with env LD_PRELOAD
// LD_PRELOAD=./preload.so ./cat cat.c
// strace -E LD_PRELOAD=./preload.so ./cat cat.c
// strace -E LD_PRELOAD=./preload.so ./cat cat.c 2>&1 | head -n 100

// Now try with LD_LIBRARY_PATH, and check the library loading order
// strace -E LD_LIBRARY_PATH=/some/library/path ./cat cat.c 2>&1 | head -n 100

// Now change the runpath
// patchelf --set-rpath /some/runpath ./cat
// strace -E LD_LIBRARY_PATH=/some/library/path ./cat cat.c 2>&1 | head -n 100

// Now run with LD_PRELAOD as well in the above same command and check the library finding order
// strace -E LD_LIBRARY_PATH=/some/library/path -E LD_PRELOAD=haha.so ./cat cat.c 2>&1 | head -n 100

// strace ./cat cat.c

