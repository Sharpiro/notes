## cross-compile

- `sudo apt install gcc-arm-linux-gnueabi`
- `arm-linux-gnueabi-gcc -o main main.c`
- `arm-linux-gnueabi-ldd main` using [[asm_arm#^cross-compile-tool|cross compile tool]]

## qemu

- `sudo apt install qemu-user`
- `export QEMU_LD_PREFIX=/usr/arm-linux-gnueabi`
- `qemu-arm -L /usr/arm-linux-gnueabi main`

## debugging

- `sudo apt install gdb-multiarch`
- `qemu-arm -g 1234 main`
- `gdb-multiarch`

```shell
# .gdbinit

set architecture armv5t
file main
set sysroot /usr/arm-linux-gnueabihf/
target remote localhost:1234
```

## tools

- [cross-compile-ldd](https://gist.github.com/jerome-pouiller/c403786c1394f53f44a3b61214489e6f) ^cross-compile-tool
    - `ldd` doesn't work well with cross compiling so this uses other tools to simulate it

## move and load

- `ldr` - load register from memory/program locations
- `mov` - move values into registers from immediate or other registers

```asm
data:
    .ascii "hello\n" // data (D) value
data_len = . - data // absolute (A) value

...

// r1 = 0x200a4
ldr r1, =data
// r2 = 6
ldr r2, =data_len
// #define data_len 6, becomes immediate value
mov r2, #data_len
```

![[asm_arm_ram_view.svg]]

## instruction format

- instructions are stored as 32 bit little endian numbers in binary
- a 32 bit instruction is parsed from least significant bit to most, 0-31, right to left
    - helps to visual the 32 bit instruction as big endian at this point

## push/pop

- push/pop are really aliases for specific store/load instructions

```asm
// sub 4 from sp, store r3 at [sp]
push {r3}    @ (str r3, [sp, #-4]!)
// load [sp] into r2, add r4 to sp
pop  {r2}    @ (ldr r2, [sp], #4)
```

## Caller vs Callee registers

- caller
    - r0-r3
    - r12
- callee
    - r4-r11
    - specials