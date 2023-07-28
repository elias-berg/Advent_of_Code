package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

func now() int64 {
	now := time.Now()
	nanos := now.UnixNano()
	return nanos / 1000000
}

func main() {
	inputFile := "input.txt"
	if len(os.Args) == 2 && os.Args[1] == "-sample" {
		inputFile = "sample_input.txt"
	}

	data, error := os.ReadFile(inputFile)
	if error != nil {
		fmt.Println(error.Error())
		return
	}

	dataStr := string(data[:])
	lines := strings.Split(dataStr, "\n")

	x := 0 // Progress in the X-direction
	y := 0 // Progress in the Y-direction
	start := now()
	for i := 0; i < len(lines); i++ {
		line := lines[i]
		commands := strings.Split(line, " ")
		dir := commands[0]
		dist, _ := strconv.Atoi(commands[1])

		if dir == "forward" {
			x += dist
		} else if dir == "up" {
			y -= dist
		} else {
			// Must be "down"
			y += dist
		}

	}
	fmt.Printf("Part 1: %d (%dms)\n", x*y, now()-start)
}
