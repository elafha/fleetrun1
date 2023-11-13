package main

import (
	"context"
	"log"
	"net/http"

	ws "github.com/gorilla/websocket"
	redis "github.com/redis/go-redis/v9"
)

var upgrader = ws.Upgrader{
	ReadBufferSize: 1024,
	WriteBufferSize: 1024,
}	

var redisClient *redis.Client
var tile38Client *redis.Client

func main (){
	redisClient = redis.NewClient(&redis.Options{
		Addr: REDIS_ADDR,
		Password: REDIS_PASSWORD,
		DB: REDIS_DB,
	})

	tile38Client = redis.NewClient(&redis.Options{
		Addr: TILE38_ADDR,
		Password: TILE38_PASSWORD,
	})

	ctx := context.Background()

	if err := redisClient.Ping(ctx).Err(); err != nil {
		panic(err)
	}

	pingCmd := redis.NewStringCmd(ctx, "PING")
	if err := tile38Client.Process(ctx, pingCmd); err != nil {
		panic(err)
	}

	http.HandleFunc(DRIVER_WS_PATH, wrapperHandler(handleDriverWs))
	http.HandleFunc(MAP_WS_PATH, wrapperHandler(handleMapWs))
	log.Fatal(http.ListenAndServe(PORT, nil))
}