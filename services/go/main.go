package main

import (
  "encoding/json"
  "math/big"
  "net/http"
  "strconv"
  "strings"
)

func fibonacci(w http.ResponseWriter, r *http.Request) {
  n, err := strconv.Atoi(strings.TrimPrefix(r.URL.Path, "/fibonacci/"))
  if err != nil || n < 0 || n > 100 { http.Error(w, `{"error":"n must be between 0 and 100"}`, 400); return }
  a, b := big.NewInt(0), big.NewInt(1)
  for i := 0; i < n; i++ { a, b = b, new(big.Int).Add(a, b) }
  w.Header().Set("Content-Type", "application/json")
  json.NewEncoder(w).Encode(map[string]any{"n": n, "value": a.String()})
}

func main() {
  http.HandleFunc("/health", func(w http.ResponseWriter) { w.Write([]byte(`{"status":"ok"}`)) })
  http.HandleFunc("/fibonacci/", fibonacci)
  http.ListenAndServe(":8000", nil)
}
