## serde

### conversion from string

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

# Clap

### Example Args

```rust
#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    /// Pattern
    #[arg(index = 2)]
    pattern: String,
    /// File
    #[arg(index = 1)]
    file: String,
    /// Number of times to greet
    #[arg(long, default_value_t = 1)]
    count: usize,
    /// Show context of matches
    #[arg(short, long)]
    context: bool,
    // a hex input
    #[arg(value_parser = parse_hex)]
    hex_val: usize,
}

fn parse_hex(arg: &str) -> Result<usize> {
    Ok(usize::from_str_radix(arg, 16)?)
}
```
