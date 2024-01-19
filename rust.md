## serde

## conversion from string

```rust
struct Track {
    #[serde(deserialize_with = "serde_this_or_that::as_f64")]
    duration: f64,
}
```

### accessing untyped json

```rs
// immutable ref returns null
let items = &res["tracks"]["items"];

// mutable ref panics
let items = &mut res["tracks"]["items"];
```

## hex formatter

- hex formatter now works in 'larger' types like arrays and structs

```rust
// debug format with 2 leading hex zeros
println!("{:02X?}", b"AZaz\0")
// pretty format with 2 leading hex zeros
println!("{:#04X?}", b"AZaz\0");
```

## useful crates

- `extend` - less boilerplate for extension methods
- `enum-as-inner` - get an enum variant as an `Option<T>` or `Result<T>`, etc.
