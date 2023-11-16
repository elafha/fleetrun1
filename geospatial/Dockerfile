FROM golang:1.20-alpine

WORKDIR /app

COPY . /app

RUN go mod download

RUN go build -o main .

EXPOSE 2110

CMD ["./main"]