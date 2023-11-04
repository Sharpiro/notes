
## lambda

```cpp
// captures 'current_char' by reference so will always have the latest value
// default is 'copy' which passes the value at lambda creation
auto process_char = [&current_char]() {
  printf("pc: %x\n", current_char);
};
```

### lambda with const

```cpp
  auto process_char = [&current_char = std::as_const(current_char),
                       &hex_value]() {
    hex_value = 99;
    current_char = 'a';
    printf("pc: %x\n", current_char);
  };
```