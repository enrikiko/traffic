# traffic
 # Fibonacci API benchmark

Benchmark the same HTTP API implemented in different runtimes (Python, Java,
Go, and optionally Rust or Node.js) using k6 on a Raspberry Pi.

## Architecture

```text
k6  ->  API under test
 |        
 +--> InfluxDB 1.x  ->  Grafana
```

The API contract is deliberately small:

```http
GET /fibonacci/100
200 OK
Content-Type: application/json

{"n":100,"value":"354224848179261915075"}
```

The value is a string so every implementation can return the exact integer
without JavaScript-number rounding. Implementations should use the same
container networking and should not include database or network calls in the
endpoint.

## Start the monitoring stack

Raspberry Pi OS 64-bit is recommended. Install Docker and the Compose plugin,
then run:

```bash
docker compose up -d influxdb grafana
```

Open Grafana at `http://<raspberry-pi-ip>:3000`. The default local login is
`admin` / `admin`; change it immediately with `GF_SECURITY_ADMIN_PASSWORD` in
`.env` before exposing the Pi outside your LAN.

## Run a benchmark

All three API implementations run at the same time. Start the complete stack:

```bash
docker compose up -d --build
```

The APIs are available from the Raspberry Pi at:

```text
Python: http://<raspberry-pi-ip>:8001
Go:     http://<raspberry-pi-ip>:8002
Java:   http://<raspberry-pi-ip>:8003
```

From the k6 container, use the Compose service names instead:

```bash
docker compose run --rm k6 run \
  --out influxdb=http://influxdb:8086/k6 \
  -e BASE_URL=http://api-python:8000 \
  /scripts/fibonacci.js
```

For an API running directly on the Pi, use `http://host.docker.internal:<port>`
and add `extra_hosts: ["host.docker.internal:host-gateway"]` to the k6 service
if your Docker version does not provide that hostname automatically.

Change `BASE_URL`, `VUS`, and `DURATION` through environment variables. The
default test is intentionally modest for a Raspberry Pi; increase load only
after checking CPU temperature and throttling.

## Fair comparison rules

- Use the same endpoint, response shape, and test profile for every language.
- Build release/production binaries and disable development reloaders.
- Run each warm-up and measurement for the same duration, preferably several
  times, and compare median/p95 latency, error rate, and requests per second.
- Record the exact implementation version, compiler/runtime version, Pi model,
  OS, and whether the service is native ARM64.

Possible additional implementations are Rust and Node.js/TypeScript. Rust is
useful as a low-overhead baseline; Node.js is useful for a highly popular
event-loop runtime.

 # Fibonacci API benchmark

Benchmark the same HTTP API in different runtimes (Python, Java, Go, and
optionally Rust or Node.js) using k6 on a Raspberry Pi.

## Contract

```http
GET /fibonacci/100
200 OK
Content-Type: application/json

{"n":100,"value":"354224848179261915075"}
```

The value is a string so every implementation returns the exact integer.

## Start

Raspberry Pi OS 64-bit is recommended. Install Docker and Compose, copy
`.env.example` to `.env`, change the Grafana password, and run:

```bash
docker compose up -d influxdb grafana
```

Open Grafana at `http://<raspberry-pi-ip>:3000`.

Start one API implementation on the Compose network, then run:

```bash
docker compose --profile tools run --rm k6 run \
  --out influxdb=http://influxdb:8086/k6 \
  -e BASE_URL=http://api-python:8000 /scripts/fibonacci.js
```

Use `http://api-python:8000`, `http://api-go:8000`, or
`http://api-java:8080` as `BASE_URL` from k6. Run separate tests against each
service while all three remain available.

The services are implemented with FastAPI/Uvicorn, Go's standard `net/http`,
and Spring Boot. Their source and Dockerfiles are under `services/`.

Use `BASE_URL`, `VUS`, and `DURATION` to select the target and load. The
default test is intentionally modest for a Raspberry Pi.

## Fair comparison

Use the same endpoint, response, test profile, and production build settings
for every language. Compare p50/p95 latency, error rate, and requests per
second, and record the Pi model, OS, runtime/compiler version, and whether the
service is native ARM64.

Rust is a useful low-overhead baseline; Node.js/TypeScript is another useful
popular event-loop runtime.
