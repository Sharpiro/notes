
## read from stdin/file

- `fgets` replaces `gets` as the secure way to read text from `stdin`

```c
char user_input[500] = {};
fgets(user_input, 25, stdin);
```

## open file

- `fopen` is still standard
- `fopen_s` is new in c11 but is not widely available

```c
  // fopen
  FILE *file = fopen("test_input.txt", "r");
  // fopen_s
  errno_t err = fopen_s(&file, "example.txt", "r");
```
## printf

```c
int main() {
    printf("hi hi\n");
    fprintf(stderr, "err: expected file\n");
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

## statically linked libc

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


## .clang-format

- `// clang-format off/on`

```yml
BasedOnStyle: LLVM
IndentWidth: 4
ContinuationIndentWidth: 4
AllowShortFunctionsOnASingleLine: None
AllowShortLambdasOnASingleLine: None
KeepEmptyLinesAtTheStartOfBlocks: false

# function alignment
AlignAfterOpenBracket: BlockIndent
BinPackParameters: false
BinPackArguments: false
AllowAllParametersOfDeclarationOnNextLine: true
PenaltyReturnTypeOnItsOwnLine: 1000000

# ternary expressions
AlignOperands: false
```

## .clangd

### Configuration

```json
// vscode settings.json
"clangd.fallbackFlags": ["-Wall"],
"clangd.arguments": ["--function-arg-placeholders=0"],
```

```yaml
// .clangd
CompileFlags: 
  Add:
    - -xc++,
    - -Wall,
    - -D_CRT_SECURE_NO_WARNINGS
    - --function-arg-placeholders=0
  Remove:
    - -Wextra
```

- `-xc`
    - forced clangd to treat files as `C`
    - This seems unnecessary until you manually specify `-std`
## simulating closures

- a [[cpp#lambda|closure]] can be simulated using structured and pointers

```cpp
void modify_with_closure(TestClosure *closure) {
  closure->result += 2;
}

int main(void) {
  TestClosure closure = {.result = 0};
  for (int i = 0; i < 4; i++) {
    printf("computed: %d\n", closure.result);
    modify_with_closure(&closure);
  }
}
```

## makefile

```makefile
CC=gcc
CFLAGS=-Wall -g -Wno-format
TARGET=sm_hash_tool
SRC_DIR=src

all: $(TARGET)

$(TARGET):  $(SRC_DIR)/*.c
	$(CC) $(CFLAGS) $(SRC_DIR)/*.c -o $(TARGET)

clean:
	rm -f $(TARGET)

```

## casts

### beware the cast position

```c
char my_char = '/'
(uint8_t)(my_char - 1) != ((uint8_t)my_char - (uint8_t)1)
```

## dereference ordering

```c
// envp is incremented, original value is sent to deref operator
char *envp[]
printf("%s\n", *(envp++));
```

## auxiliary vector

```c
#include <elf.h>
#include <stdio.h>

int main(int argc, char *args[], char *envp[]) {
  while (*envp++ != NULL) {
  }

  Elf64_auxv_t *auxv = (Elf64_auxv_t *)envp;
  while (auxv->a_type != AT_NULL) {
    printf("%p, %lu, 0x%lx\n", auxv, auxv->a_type, auxv->a_un.a_val);
    auxv++;
  }
}

```

## include math

for some reason clang doesn't link with math standard library by default

```sh
clang -lm main main.c
```

## clang blocks

- `sudo dnf install libblocksruntime-devel`
- `clang block.c -fblocks -lBlocksRuntime`

```c
#include <Block.h>

int main(void) {
  int x = 1;
  int (^f)(int) = ^int(int y) {
    return x + y;
  };

  return f(1);
}
```

## inline asm

- move variable into register

```c
uint64_t x = 0;
// refer to by name
asm("mov rdi, %[x]" : : [x] "r"(x));
// refer to by position
asm("mov rdi, %0" : : "r"(x));
```

## misc

- `-mno-sse`
    - disable "Streaming SIMD Extensions" instructions which apparently require libc initialization

## statically linked library

```sh
# create object file
gcc -c -o file1.o file1.c
# pack multiple object files into static lib
ar rcs libmystatic.a file1.o file2.o
# use static lib
gcc -o temp temp.c libmystatic.a
```

## Building Clang

### Prerequisites

```sh
sudo apt install cmake
```

### Build

```sh
git clone --depth 1 --branch release/19.x https://github.com/llvm/llvm-project.git
mkdir llvm-project/build
cd llvm-project/build
time CC=/opt/gcc-14.1.0/bin/gcc CXX=/opt/gcc-14.1.0/bin/g++ cmake -DLLVM_ENABLE_PROJECTS="clang;clang-tools-extra;lld;lldb;polly;compiler-rt" -DLLVM_ENABLE_RUNTIMES="all" -DCMAKE_BUILD_TYPE="Release" -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="/opt/clang-19.x" -DLLVM_TARGETS_TO_BUILD="ARM;AArch64" -DLLVM_HOST_TRIPLE="arm-linux-gnueabihf" ../llvm
time make -j6
sudo make install
```

- `DLLVM_HOST_TRIPLE`
    - Most important triple when ambiguous like arm32
- `LLVM_DEFAULT_TARGET_TRIPLE`
    - Not needed when `DLLVM_HOST_TRIPLE` is set
- `DLLVM_ENABLE_RUNTIMES`
    - required for `compiler-rt` sanitizers
- `--gcc-install-dir`
    - clang executable option to specify gcc install

## Building GCC

### Prerequisites

- try downloading prerequisites via `./contrib/download_prerequisites`

#### Raspbian

```sh
sudo apt install build-essential libgmp-dev32 libmpfr-dev libmpc-dev flex
```

### Build

```sh
git clone --depth 1 --branch releases/gcc-14.1.0 git://gcc.gnu.org/git/gcc.git
mkdir gcc/build
cd gcc/build
../configure \
    --build=arm-linux-gnueabihf \
    --host=arm-linux-gnueabihf \
    --prefix=/opt/gcc-14.1.0 \
    --enable-languages=c,c++ \
    --disable-multilib \
    --enable-checking=release
time make -j6
sudo make install
```

- `--build` required for arm32 since it doesn't detect correctly
    - unclear if `host` is also needed with this specified
- `--host` required for arm32 since it doesn't detect correctly

## Qemu

- `qemu-user`
- `gcc-arm-linux-gnueabihf` arm toolchain/sysroot
- `gdb-multiarch`

### Compiling

#### Prerequisites

- `libglib2.0-dev bison ninja-build python3-pip`
### Build

```sh
mkdir build
cd build
../configure \
    --prefix=/opt/qemu-8.2.2 \
    --disable-werror
time make -j6
```
