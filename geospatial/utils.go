package main

import (
	"encoding/json"
	"fmt"
	// "strings"
	"errors"
	"net/http"
	// jwt "github.com/dgrijalva/jwt-go"
)

var errInvalidFormat = errors.New("invalid format")
// var errMissingAuthorization = errors.New("missing authorization header")
// var errInvalidAuthorization = errors.New("invalid authorization header")

func parseLocationMessage(msg []byte) (p Point, err error) {
	var m Point
	if err := json.Unmarshal(msg, &m); err != nil {
		return Point{}, err
	}

	if !m.Valid() {
		return Point{}, errInvalidFormat
	}

	return m, nil
}

func parseBBoxMessage(msg []byte) (b BBox, err error) {
	var m BBox
	if err := json.Unmarshal(msg, &m); err != nil {
		return BBox{}, err
	}

	if !m.Valid() {
		return BBox{}, errInvalidFormat
	}

	return m, nil
}

func validateRequest(r *http.Request) (id string, err error) {
	// auth := r.Header.Get("Authorization")
	// if auth == "" {
	// 	return "", errMissingAuthorization
	// }

	// parts := strings.Split(auth, " ")
	// if len(parts) != 2 {
	// 	return "", errInvalidAuthorization
	// }

	// token := parts[1]
	// claims := jwt.MapClaims{}
	// _, err = jwt.ParseWithClaims(token, claims, func(token *jwt.Token) (interface{}, error) {
	// 	return []byte(PUBLIC_JWT_KEY), nil
	// })

	// if err != nil {
	// 	return "", errInvalidAuthorization
	// }

	// return claims["id"].(string), nil
	return "1", nil
}

func wrapperHandler(h func(w http.ResponseWriter, r *http.Request) error) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if err := h(w, r); err != nil {
			fmt.Println("FAIL: ", err)
			http.Error(w, err.Error(), http.StatusBadRequest)
		}
	}
}