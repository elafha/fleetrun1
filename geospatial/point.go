package main

type Point struct {
	Lng float64 `json:"lng"`
	Lat float64 `json:"lat"`
}

func (p Point) Valid() bool {
	if p.Lat < -90 || p.Lat > 90 {
		return false
	}
	if p.Lng < -180 || p.Lng > 180 {
		return false
	}
	return true
}