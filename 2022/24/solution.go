// Advent of Code 2022 - Day 24
// Blizzard Basin
//
// On the way to the extraction point, now that all the star fruit are planted
// for next year, you come across a blizzard field. The blizzards are going in
// one direction, each, infinitely, and when they reach a wall, they go back to
// the opposite wall and repeat the process. You need to cross the field, going
// from the top-left entrance to the bottom-right exit. You can't be in a space
// with a blizzard at the same time, though, so you can only move into spaces
// unoccupied by any blizzards.
//
// Part 1 -
// What is the least number of steps it takes to get from the start to the end?
//
// Part 2 -
// One of the elves forgot his snacks at the entrance of the field...
// What's the least number of steps it takes to get from start to end, back to
// start, and then back to the end again?

// To run:
// - 'go run solution.go'
// - 'go run solution.go -sample' to run the sample input

package main

import (
	"fmt"
	"math"
	"os"
	"strings"
)

type Space struct {
	x      int
	y      int
	bliz   []byte
	isWall bool
}

// Helper function to actually set a spot in the next iteration given the
// original grid and the current position of a blizzard we're trying to move.
func setNextBlizSpot(grid [][]*Space, next [][]*Space, x int, y int) {
	s := grid[y][x]
	for b := 0; b < len(s.bliz); b++ {
		char := s.bliz[b]
		nx := x
		ny := y

		if char == '<' {
			nx = nx - 1
			if nx == 0 {
				nx = len(grid[y]) - 2
			}
		}
		if char == '>' {
			nx = nx + 1
			if nx == len(grid[y])-1 {
				nx = 1
			}
		}
		if char == 'v' {
			ny = y + 1
			if ny == len(grid)-1 {
				ny = 1
			}
		} else if char == '^' {
			ny = y - 1
			if ny == 0 {
				ny = len(grid) - 2
			}
		}

		next[ny][nx].bliz = append(next[ny][nx].bliz, char)
	}
}

// Given the blizzard grid, goes through and calculates the next iteration of
// the grid by going through each position and moving each blizzard one space
// into a new copy of the blizzard grid in order to preserve every position.
func moveBlizzards(grid [][]*Space) [][]*Space {
	var nextBliz [][]*Space

	// First, create a clean copy
	for y := 0; y < len(grid); y++ {
		var row []*Space
		for x := 0; x < len(grid[y]); x++ {
			s := new(Space)
			s.x = x
			s.y = y
			s.isWall = grid[y][x].isWall
			row = append(row, s)
		}
		nextBliz = append(nextBliz, row)
	}

	// Now move all the blizzards from grid -> nextBliz
	for y := 1; y < len(grid)-1; y++ { // Skip the first and last rows
		for x := 0; x < len(grid[y]); x++ {
			setNextBlizSpot(grid, nextBliz, x, y)
		}
	}

	return nextBliz
}

// Helper function to print the state of the blizzard grid.
// For debugging.
func printBliz(grid [][]*Space) {
	for y := 0; y < len(grid); y++ { // Skip the first and last rows
		for x := 0; x < len(grid[y]); x++ {
			s := grid[y][x]
			if s.isWall {
				fmt.Print("#")
			} else {
				cnt := len(s.bliz)
				if cnt == 0 {
					fmt.Print(".")
				} else if cnt == 1 {
					fmt.Print(string(s.bliz[0]))
				} else {
					fmt.Print(cnt)
				}
			}
		}
		fmt.Println()
	}
}

// Recursive function to navigate the blizzard grid in a DFS fashion.
// Note that it may be wiser to do this as a BFS saving the state of the blizzard grid at each step...
func navigateBlizzards(blizzards [][][]*Space, cur *Space, moves int, endX int, endY int, best *int, visited map[string]bool) {
	// Step 1) Move the blizzards
	move := moves + 1
	next := blizzards[move%len(blizzards)]

	// Base case 0: we've been here at this same relative point in time before...
	key := fmt.Sprintf("%d-%d,%d", moves, cur.x, cur.y)
	if visited[key] {
		return
	}
	visited[key] = true

	// Base case 1: we've reached the end
	if cur.y == endY && cur.x == endX {
		if moves < *best {
			*best = moves
		}
		return
	}
	// Base case 2: we've surpassed the best we've seen so far; not worth continuing
	if moves > *best {
		return
	}
	// Base case 3: the distance from the end is greater than the current best
	if (endY-cur.y)+(endX-cur.x)+move > *best {
		return
	}

	// Else, get on with the calculating
	// Step 2) Move yourself
	// - Always prioritize right and down
	// - Try waiting if you can't move right/down
	// - Otherwise, move up or left
	var nextSpaces []*Space
	nextSpace := next[cur.y][cur.x+1] // Right
	if !nextSpace.isWall && len(nextSpace.bliz) == 0 {
		nextSpaces = append(nextSpaces, nextSpace)
	}
	// Down (we need to worry about going off-screen)
	if cur.y < len(next)-1 {
		nextSpace = next[cur.y+1][cur.x]
		if !nextSpace.isWall && len(nextSpace.bliz) == 0 {
			nextSpaces = append(nextSpaces, nextSpace)
		}
	}
	nextSpace = next[cur.y][cur.x] // Wait
	if !nextSpace.isWall && len(nextSpace.bliz) == 0 {
		nextSpaces = append(nextSpaces, nextSpace)
	}
	nextSpace = next[cur.y][cur.x-1] // Left
	if !nextSpace.isWall && len(nextSpace.bliz) == 0 {
		nextSpaces = append(nextSpaces, nextSpace)
	}
	// Up (we need to worry about going off-screen)
	if cur.y > 0 {
		nextSpace = next[cur.y-1][cur.x] // Get the next state of the current spot
		if !nextSpace.isWall && len(nextSpace.bliz) == 0 {
			nextSpaces = append(nextSpaces, nextSpace)
		}
	}

	// If we're going back to the start, reverse the directions we prioritize
	if endY == 0 {
		for i, j := 0, len(nextSpaces)-1; i < j; i, j = i+1, j-1 {
			nextSpaces[i], nextSpaces[j] = nextSpaces[j], nextSpaces[i]
		}
	}

	for i := 0; i < len(nextSpaces); i++ {
		navigateBlizzards(blizzards, nextSpaces[i], move, endX, endY, best, visited)
	}
}

// Checks if two blizzard grid spaces are exactly the same.
func equals(a *Space, b *Space) bool {
	if len(a.bliz) != len(b.bliz) {
		return false
	}
	for i := 0; i < len(a.bliz); i++ {
		if a.bliz[i] != b.bliz[i] {
			return false
		}
	}
	return true
}

// Checks if two blizzard grids are exactly the same.
func checkSame(a [][]*Space, b [][]*Space) bool {
	for y := 0; y < len(a); y++ {
		for x := 0; x < len(a[y]); x++ {
			if !equals(a[y][x], b[y][x]) {
				return false
			}
		}
	}
	return true
}

func main() {
	inputFile := "input.txt"
	if len(os.Args) == 2 && os.Args[1] == "-sample" {
		inputFile = "sample_input.txt"
	}

	// File reading
	data, error := os.ReadFile(inputFile)
	if error != nil {
		fmt.Println(error.Error())
		return
	}

	var grid [][]*Space

	// Convert the byte array to a line-by-line string
	dataStr := string(data[:])
	lines := strings.Split(dataStr, "\n")
	for i := 0; i < len(lines); i++ {
		var row []*Space
		line := lines[i]
		for j := 0; j < len(line); j++ {
			space := new(Space)
			space.x = j
			space.y = i

			char := line[j]
			if char == '#' {
				space.isWall = true
			} else {
				if char != '.' {
					space.bliz = append(space.bliz, char)
				}
			}
			row = append(row, space)
		}
		grid = append(grid, row)
	}

	// I figure there can only be so many configurations of blizzards, so we're going to
	// try and calculate them all up-front, which wouldn't fly if we had an enormous grid.
	var allBlizzards [][][]*Space
	allBlizzards = append(allBlizzards, grid)
	for i := 0; i < 1; {
		next := moveBlizzards(allBlizzards[len(allBlizzards)-1])
		if !checkSame(next, allBlizzards[0]) {
			allBlizzards = append(allBlizzards, next)
		} else {
			i = 1
		}
	}

	// Now that we have the blizzard grid, recursively try to figure out the
	// fastest path to the end
	var best int = math.MaxInt
	visited := make(map[string]bool)
	endY := len(grid) - 1
	endX := len(grid[0]) - 2
	navigateBlizzards(allBlizzards, allBlizzards[0][0][1], 0, endX, endY, &best, visited)

	fmt.Printf("Part 1: %d\n", best)

	// For Part 2, we need to get back to the start to get those damn snacks...
	var toStart int = math.MaxInt
	visited = make(map[string]bool)
	navigateBlizzards(allBlizzards, allBlizzards[best%len(allBlizzards)][endY][endX], best, 1, 0, &toStart, visited)
	// And then back to the end again!
	var toEnd int = math.MaxInt
	visited = make(map[string]bool)
	navigateBlizzards(allBlizzards, allBlizzards[toStart%len(allBlizzards)][0][1], toStart, endX, endY, &toEnd, visited)

	fmt.Printf("Part 2: %d\n", toEnd)

}
