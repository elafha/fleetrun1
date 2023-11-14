package main

import (
	"context"
	"encoding/json"
	"net/http"

	set "github.com/deckarep/golang-set"

	ws "github.com/gorilla/websocket"
	t38 "github.com/xjem/t38c"
)

var listeners = set.NewSet()

type DriverUpdate struct {
	DriverId string `json:"id"`
	Location Point `json:"location"`
	Action t38.DetectAction `json:"action"`
}

func setListener(ctx context.Context, b BBox, listenerId string) error {
	geofenceRequest := tile38Client.Geofence.Within(UPDATE_CHANNEL).Bounds(b.MinLat, b.MinLng, b.MaxLat, b.MaxLng).Actions(t38.Inside, t38.Exit, t38.Enter)
	if err := tile38Client.Channels.SetChan(listenerId, geofenceRequest).Do(ctx); err != nil {
		return err
	}
	return nil
}

func removeListener(ctx context.Context, listenerId string) error {
	if err := tile38Client.Channels.DelChan(ctx, listenerId); err != nil {
		return err
	}
	listeners.Remove(listenerId)
	return nil
}

func handleGeoFenceEvent(ctx context.Context, conn *ws.Conn) t38.EventHandler {
	return t38.EventHandlerFunc(func(e *t38.GeofenceEvent) error {
		driverUpdate := DriverUpdate{
			DriverId: e.ID,
			Location: Point{
				Lat: e.Point.Lat,
				Lng: e.Point.Lon,
			},
			Action: t38.DetectAction(e.Detect),
		}
		msg, err := json.Marshal(driverUpdate)
		if err != nil {
			return err
		}


		if err := conn.WriteMessage(ws.TextMessage, msg); err != nil {
			return err
		}

		return nil
	})
}

func listen(ctx context.Context, listenerId string, conn *ws.Conn, client *t38.Client) error {
	if listeners.Contains(listenerId) {
		return nil
	}
	listeners.Add(listenerId)

	if err := client.Channels.Subscribe(ctx, handleGeoFenceEvent(ctx, conn),listenerId); err != nil {
		return err
	}

	return nil
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

	client, err := t38.New(t38.Config{
		Address: TILE38_ADDR,
	})
	if err != nil {
		return err
	}
	defer client.Close()

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

		b, err := parseBBoxMessage(msg)
		if err != nil {
			return err
		}

		if err := setListener(r.Context(), b, id); err != nil {
			return err
		}

		go listen(r.Context(), id, conn, client)
	}
}