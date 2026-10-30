
#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-go}"
VUS="${2:-${VUS:-100}}"
DURATION="${3:-${DURATION:-600s}}"
run_test() {
  local name="$1"; local base_url="$2"
  echo "Running ${name}: ${VUS} VUs for ${DURATION}"
  docker compose --profile tools run --rm -e BASE_URL="${base_url}" -e VUS="${VUS}" -e DURATION="${DURATION}" k6 run --out influxdb=http://influxdb:8086/k6 /scripts/fibonacci.js
}
case "${TARGET}" in
  go) run_test "Go" "http://api-go:8000" ;;
  java) run_test "Java" "http://api-java:8080" ;;
  python) run_test "Python" "http://api-python:8000" ;;
  rust) run_test "Rust" "http://api-rust:8000" ;;
  all) run_test "Go" "http://api-go:8000"; run_test "Java" "http://api-java:8080"; run_test "Python" "http://api-python:8000"; run_test "Rust" "http://api-rust:8000" ;;
  *) echo "Usage: $0 [go|java|python|rust|all] [vus] [duration]" >&2; exit 2 ;;
esac
