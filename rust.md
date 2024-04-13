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

## Clap

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
