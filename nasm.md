## string and length

```asm
section .data
	msg db `Hello, World!\n`
	msg_len equ $ - msg
```

## `jmp`

in some situations a jump needs to be calculated with (address - instruction_size) because after the jump is made, the instruction pointer will immediately be incremented, possibly moving 1 instruction passed the one you meant to execute next

### jmp - absolute

Will jump to instruction at `0x401020` as expected

```asm
jmp    0x401020
```

### jmp - register relative

Will jump to instruction at the dereference of `rsp+0x8` as expected

```asm
jmp    QWORD PTR [rsp+0x8]
```
### jmp - rip relative

seems to always be off by 6, implying the `rip` register is being incremented earlier than even gdb says.

gdb when at this instruction evaluates `rip+0x2fe2` to be `0x404012`, 6 bytes short of the `0x404018` address it will dereference then jump to.

```asm
jmp    QWORD PTR [rip+0x2fe2] # 0x404018 <printf@got.plt>
```