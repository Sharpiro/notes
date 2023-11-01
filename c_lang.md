## printf

```c
int main() {
	printf("hi hi\n");
}
```


## mmap for executable memory

```c
void *buffer = mmap(NULL, size, PROT_READ | PROT_WRITE | PROT_EXEC,
	MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
```

## view memory maps

```c
pgrep -a main
cat /proc/369121/maps
```

## read from unknown file size

```c
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define CHUNK_SIZE 100
#define BUFFER_LEN 5000

int main(int argc, char **args) {
    FILE *file = popen("cat ../main.c", "r");
    char *buffer = malloc(BUFFER_LEN);
    size_t index = 0;
    size_t read_result;
    while ((read_result = fread(buffer + index, 1, CHUNK_SIZE, file))) {
        index += read_result;
        if (index >= BUFFER_LEN) {
            printf("out of mem\n");
            exit(1);
        }
    }

    printf("%s\n", buffer);
    printf("%ld\n", index);

    pclose(file);
    free(buffer);
}
```

## statically linked c

```sh
sudo dnf install glibc-static
gcc -static main.c
```

## relocate program with linker

relocating `.interp` section seems to affect the whole program's offset

```sh
gcc -Wall -g -o test.exe \
-Wl,--section-start=.interp=0x800000 \
test_program.c
```