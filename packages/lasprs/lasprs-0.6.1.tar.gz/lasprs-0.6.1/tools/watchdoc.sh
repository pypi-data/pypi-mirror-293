#!/bin/bash

# Required is cargo-watch and http:
#
# ```bash
# $ cargo install cargo-watch cargo-docserver`
# ```
#
cargo watch -s "clear && cargo doc --no-deps -p lasprs --lib && cargo docserve"

# Then open: ${browser} http://localhost:4000
