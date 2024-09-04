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

## PC-relative instructions

- in GDB, `$pc` equals the address of the current instruction about to be executed no matter the architecture.
- However in ARM32 under the hood, `$pc` is actually 2 instructions ahead due to pipelining
    - Note: This is allegedly not true in ARM64, and thus would be more straightforward
- Consider the ARM32 example `0x100a8 add r12, pc, #0`
    - The answer seems obviously to be `$r12 = 0x100a8`
    - However due to the "+8" from pipelining, the answer is actually `$r12 = 0x100b0`

## Branching

- `b` - branch to given address
- `bl` - set `lr` to next instruction then branch to given address
    - `bl 0x1000`
- `bx` - branch to given register, optionally switch b/w arm/thumb
    - `bx lr`

### Misc

- A pre-indexed writeback occurs before the load is performed
    - ex: `ldr r3, [r3, #4]!`
    ```c
    writeback_value = r3 + 4
    deref_value = *(r3 + 4)
    r3 = writeback_value // immediately overwritten
    r3 = deref_value
    ````
    - this is never really done and assembler gives a warning

## References

- Instruction Set
    - [[arm_iso_1.pdf]] [web](https://iitd-plos.github.io/col718/ref/arm-instructionset.pdf)
    - [[arm_iso_2.pdf]] [web](https://profile.iiita.ac.in/bibhas.ghoshal/COA_2021/lecture_slides/arm_inst.pdf)
- [Immediate rotation](https://alisdair.mcdiarmid.org/arm-immediate-value-encoding/)
- [CPSR Register](https://developer.arm.com/documentation/ddi0601/2023-12/AArch32-Registers/CPSR--Current-Program-Status-Register)
