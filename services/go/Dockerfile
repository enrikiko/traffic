FROM golang:1.23-alpine AS build
WORKDIR /src
COPY go.mod main.go ./
RUN CGO_ENABLED=0 go build -o /fibonacci .
FROM alpine:3.21
COPY --from=build /fibonacci /fibonacci
EXPOSE 8000
ENTRYPOINT ["/fibonacci"]
