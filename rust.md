## Lifetimes

- `-> impl FnMut(&[u8]) -> NomResult<usize> + '_`
    - The closure should borrow any referenced data for the shortest possible lifetime
    - This often ties the closure's lifetime to the lifetime of the inputs it captures by reference

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

## Clap

### Args Example

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

### Subcommand Example

```rust
#[derive(Parser)]
#[command(version, about, long_about = None)]
#[command(propagate_version = true)]
struct Cli {
    /// Path to rom file
    #[arg(long)]
    rom: String,
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Dumps Rom Info
    Dump {
        /// Temp arg
        #[arg(long)]
        temp: Option<String>,
    },
    /// Analyzes Rom
    Analyze,
}
```

## Tauri

### Builder boilerplate

```rust
#[tauri::command]
#[specta::specta]
fn read_file(path: &str) -> Result<(u32, bool, String), MyErr> {
    read_file_internal(path)
        .with_context(|| path.to_string())
        .map_err(|e| MyErr {
            message: e.to_string(),
        })
}

fn main() {
    let specta_builder = {
        let specta_builder = tauri_specta::ts::builder()
            .config(
                ExportConfig::new().bigint(BigIntExportBehavior::FailWithReason(
                    "bigint currently unsupported",
                )),
            )
            .commands(tauri_specta::collect_commands![read_file]);

        #[cfg(debug_assertions)]
        let specta_builder = specta_builder.path("../src/bindings.ts");

        specta_builder.into_plugin()
    };
    tauri::Builder::default()
        .plugin(specta_builder)
        .setup(|app| {
            #[cfg(debug_assertions)]
            {
                let window = app.get_window("main").unwrap();
                window
                    .set_size(Size::Logical(LogicalSize {
                        width: 1200.0,
                        height: 800.0,
                    }))
                    .unwrap();
                window.open_devtools();
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![read_file])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Build file - `build.rs`

- Caching
    - `println!("cargo:rerun-if-changed=build.rs");`
    - Speeds up build so `build.rs` only re-runs if file changed
- Logging
    - `println!("cargo:warning={x:?}");`

## Nom

- Usually use imports from `nom::bytes::complete` instead of `nom::complete`

### Parsers

- `take`: take a certain number of bytes

## Unsafe Rust

- Always check null pointers before passing them to unsafe functions

## Logging

- `tracing_subscriber`
    - `env-filter`
- `tracing`

```rust
    // export RUST_LOG=info,my_mod=trace
    tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::from_default_env())
        .with_target(false)
        .without_time()
        .init();
```

## Return temporary array from function

```rust
fn get_state(&self) -> &[u32] {
    // state: u32
    std::array::from_ref(&self.state)
}
```
## Crates

- `extend` - less boilerplate for extension methods
- `enum-as-inner` - get an enum variant as an `Option<T>` or `Result<T>`, etc.
- `enum-dispatch`
    - allows an enum to auto-implement a trait if all variants implement that trait
- `num-enum` - number/enum conversion
- `strum` - macros for string/enum conversion
- `const_format` - formatting strings at compile-time
- `static_assertions` - static/const assertions
- `bindgen` - create rust bindings from c
- `cbindgen` - create c/c++ bindings from rust
- `inotify` - low level Linux fs events
- `notify` - Cross platform fs events
- regex
    - [regex](https://crates.io/crates/regex)
    - [fancy-regex](https://crates.io/crates/fancy-regex) - Supports slower features like backreferences and look-arounds
- tracing/logging
    - `tracing` + `tracing_subscriber`
- `indexmap` - `HashMap` and `HashSet` but they maintain their order
- `zerocopy` - Safe C-like casting of buffers to struct pointers
- `bytemuck` - Similar to `zerocpy` but more focused on packing w/o padding
- `num-format` - format commas
- `pretty_hex`- pretty hex
