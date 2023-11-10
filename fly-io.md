
## rust builds broken w/ ssl error

- [fly forum](https://community.fly.io/t/rust-server-missing-libssl-so-3-on-new-deploy/15114/4)

```dockerfile
FROM rust:bookworm as builder
...
FROM debian:bookworm-slim
```