package main

import (
	"context"
	"log"
	"net/http"

	ws "github.com/gorilla/websocket"
	redis "github.com/redis/go-redis/v9"
	t38 "github.com/xjem/t38c"
)

var upgrader = ws.Upgrader{
	ReadBufferSize: 1024,
	WriteBufferSize: 1024,
	CheckOrigin: checkOrigin,
}	

var redisClient *redis.Client
var tile38Client *t38.Client

func main (){
	redisClient = redis.NewClient(&redis.Options{
		Addr: REDIS_ADDR,
		Password: REDIS_PASSWORD,
		DB: REDIS_DB,
	})
	if status := redisClient.Ping(context.Background()); status.Err() != nil {
		log.Fatal(status.Err())
	}
	defer redisClient.Close()

	var err error
	tile38Client, err = t38.New(t38.Config{
		Address: TILE38_ADDR,
	})
	if err != nil {
		log.Fatal(err)
	}
	defer tile38Client.Close()

	http.HandleFunc(DRIVER_WS_PATH, wrapperHandler(handleDriverWs))
	http.HandleFunc(MAP_WS_PATH, wrapperHandler(handleMapWs))
	log.Fatal(http.ListenAndServe(PORT, nil))
}