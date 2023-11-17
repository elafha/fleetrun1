package main

import (
	"net/http"
)

func checkOrigin(r *http.Request) bool {
	return true
}