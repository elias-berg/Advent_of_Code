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

func part1(lines []string) int {
	x := 0 // Progress in the X-direction
	y := 0 // Progress in the Y-direction
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
	return x * y
}

func part2(lines []string) int {
	// All things considered, I could just process part 2 as a part of the
	// loop in part 1, but we'll just copy and paste to keep it cleaner.
	x := 0
	y := 0
	a := 0 // 'a' is short for "aim" here
	for i := 0; i < len(lines); i++ {
		line := lines[i]
		commands := strings.Split(line, " ")
		dir := commands[0]
		dist, _ := strconv.Atoi(commands[1])

		if dir == "up" {
			a -= dist
		} else if dir == "down" {
			a += dist
		} else {
			// Must be "forward"
			x += dist
			y += a * dist
		}
	}
	return x * y
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

	start := now()
	fmt.Printf("Part 1: %d (%dms)\n", part1(lines), now()-start)

	start = now()
	fmt.Printf("Part 2: %d (%dms)\n", part2(lines), now()-start)
}
