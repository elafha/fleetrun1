package main

import (
	"net/http"
	"context"
	set "github.com/deckarep/golang-set"
	
	redis "github.com/redis/go-redis/v9"
	ws "github.com/gorilla/websocket"
)

type BBox struct {
	MinLat float64 `json:"min_lat"`
	MinLng float64 `json:"min_lng"`
	MaxLat float64 `json:"max_lat"`
	MaxLng float64 `json:"max_lng"`
}

var listeners = set.NewSet()

func (b BBox) Valid() bool {
	return b.MinLat != 0 && b.MinLng != 0 && b.MaxLat != 0 && b.MaxLng != 0
}

func setListener(ctx context.Context, b BBox, listenerId string) error {
	cmd := redis.NewCmd(ctx, "SETCHAN", listenerId, "WITHIN", UPDATE_CHANNEL, "FENCE", "DETECT", "inside,exit,enter", "BOUNDS", b.MinLat, b.MinLng, b.MaxLat, b.MaxLng)
	if err := tile38Client.Process(ctx, cmd); err != nil {
		return err
	}
	return nil
}

func removeListener(ctx context.Context, listenerId string) error {
	cmd := redis.NewCmd(ctx, "DELCHAN", listenerId)
	if err := tile38Client.Process(ctx, cmd); err != nil {
		return err
	}
	listeners.Remove(listenerId)
	return nil
}

func listen(ctx context.Context, listenerId string, conn *ws.Conn) error {
	if listeners.Contains(listenerId) {
		return nil
	}

	listeners.Add(listenerId)
	cmd := redis.NewCmd(ctx, "SUBSCRIBE", listenerId)
	if err := tile38Client.Process(ctx, cmd); err != nil {
		return err
	}

	for {
		msg, err := cmd.Result()
		if err != nil {
			return err
		}

		msgBytes, ok := msg.([]byte)
		if !ok {
			continue
		}

		if err := conn.WriteMessage(ws.TextMessage, []byte(msgBytes)); err != nil {
			return err
		}
	}
}

func handleMapWs(w http.ResponseWriter, r *http.Request) error {
	id, err := validateRequest(r)

	if err != nil {
		return err
	}

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil{
		return err
	}
	defer conn.Close()
	defer removeListener(r.Context(), id)

	for {
		msgType, msg, err := conn.ReadMessage()
		if err != nil {
			return err
		}

		if msgType != ws.TextMessage {
			return errInvalidFormat
		}

		b, err := parseBBoxMessage(msg)
		if err != nil {
			return err
		}

		if err := setListener(r.Context(), b, id); err != nil {
			return err
		}

		go listen(r.Context(), id, conn)
	}
}