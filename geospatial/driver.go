package main

import (
	"context"
	"net/http"

	ws "github.com/gorilla/websocket"
	redis "github.com/redis/go-redis/v9"
)

func publishLocationUpdate(ctx context.Context, driverId string, location Point) error {
	if err := tile38Client.Keys.Set(UPDATE_CHANNEL, driverId).Point(location.Lat, location.Lng).Do(ctx); err != nil {
		return err
	}
	return nil
}

func updateDriverLocation(ctx context.Context, id string, p Point) error {
	err := redisClient.GeoAdd(ctx, DRIVERS_KEY, &redis.GeoLocation{
		Name: id,
		Latitude: p.Lat,
		Longitude: p.Lng,
	}).Err()

	if err != nil {
		return err
	}

	err = publishLocationUpdate(ctx, id, p)
	
	if err != nil {
		return err
	}

	return nil
}

func handleDriverWs(w http.ResponseWriter, r *http.Request) error {
	id, err := validateRequest(r)

	if err != nil {
		return err
	}

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil{
		return err
	}
	defer conn.Close()

	for {
		msgType, msg, err := conn.ReadMessage()

		if err != nil {
			return err
		}

		if msgType == ws.PingMessage{
			conn.WriteMessage(ws.PongMessage, []byte{})
			continue
		}

		if msgType == ws.PongMessage {
			continue
		}

		if msgType == ws.CloseMessage {
			return nil
		}

		if msgType != ws.TextMessage {
			return errInvalidFormat
		}

		p, err := parseLocationMessage(msg)

		if err != nil {
			return err
		}

		if err := updateDriverLocation(r.Context(), id, p); err != nil {
			return err
		}
	}
}