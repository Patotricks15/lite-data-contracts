# SDKs

Every Lite library exposes the same integration model: Rust is the source of truth; Python builds wheels with `maturin`, Node.js builds native modules with `napi-rs`, and Go links a versioned C ABI through cgo. Keep marshaling at the edge and pass JSON only where a typed language model is not practical.