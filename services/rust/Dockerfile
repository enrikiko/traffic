FROM rust:1.87-bookworm AS build
WORKDIR /src
COPY Cargo.toml .
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim
COPY --from=build /src/target/release/fibonacci-api /usr/local/bin/fibonacci-api
EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/fibonacci-api"]

