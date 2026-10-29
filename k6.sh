docker compose --profile tools run --rm k6 run \
  --out influxdb=http://192.168.1.245:8086/k6 \
  -e BASE_URL=http://api-python:8000 \
  /scripts/fibonacci.js