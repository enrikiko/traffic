use axum::{extract::Path, http::StatusCode, response::IntoResponse, routing::get, Json, Router};
use num_bigint::BigUint;
use serde::Serialize;

#[derive(Serialize)]
struct FibonacciResponse { n: u32, value: String }

#[derive(Serialize)]
struct ErrorResponse { error: &'static str }

async fn health() -> Json<serde_json::Value> { Json(serde_json::json!({"status": "ok"})) }

async fn fibonacci(Path(n): Path<i32>) -> impl IntoResponse {
    if !(0..=100).contains(&n) {
        return (StatusCode::BAD_REQUEST, Json(serde_json::json!(ErrorResponse { error: "n must be between 0 and 100" })));
    }
    let (mut a, mut b) = (BigUint::from(0u32), BigUint::from(1u32));
    for _ in 0..n { let next = &a + &b; a = b; b = next; }
    (StatusCode::OK, Json(serde_json::json!(FibonacciResponse { n: n as u32, value: a.to_string() })))
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/health", get(health)).route("/fibonacci/{n}", get(fibonacci));
    let listener = tokio::net::TcpListener::bind("0.0.0.0:8000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

