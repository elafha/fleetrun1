package main

type BBox struct {
	MinLat float64 `json:"min_lat"`
	MinLng float64 `json:"min_lng"`
	MaxLat float64 `json:"max_lat"`
	MaxLng float64 `json:"max_lng"`
}

func (b BBox) Valid() bool {
	return b.MinLat != 0 && b.MinLng != 0 && b.MaxLat != 0 && b.MaxLng != 0
}