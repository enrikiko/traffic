FROM golang:1.23-alpine AS build
WORKDIR /src
COPY main.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /fibonacci main.go
FROM alpine:3.21
COPY --from=build /fibonacci /fibonacci
EXPOSE 8000
ENTRYPOINT ["/fibonacci"]
