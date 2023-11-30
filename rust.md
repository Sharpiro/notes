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