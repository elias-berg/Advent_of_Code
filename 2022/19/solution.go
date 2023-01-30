// Advent of Code 2022 - Day 19
// Not Enough Minerals
//
// The lava stops flowing in your direction, so now you can escape with the elephants.
// However, you notice a pond with geodes you'd like to collect. In order to make a
// geode-cracking robot, you need obsidian. In order to get obsidian, you need an
// obsidian-collecting robot that must be waterproof with clay. In order to collect clay,
// you need a clay-collecting robot that must be made with ore. You start with one ore-
// collecting robot and a series of blueprints (the input) that can be used to determine
// how many resources each robot takes to be created.
//
// Part 1 -
// You have 24 minutes until the elephants get too hungry, so you want to go through all
// of the blueprints to find out what series of robot collection and building will grant
// you the most number of geodes, per blueprint. Given a "quality" number of the blueprint
// id (blueprint #) multiplied by the max number of geodes the blueprint can collect in 24
// minutes, what is the sum of every blueprint's quality number?

// To run:
// - Make sure you have Go installed on your machine
// - Use the command: 'go run solution.go'
// - Additionally, you can add '-sample' to run the sample input: 'go run solution.go -sample'

package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

/**
 * Parses the given input file and returns the blueprints as an array of integer arrays.
 * Based on the input, each array should be exactly 7 in length, where each index
 * denotes the following:
 * 0 = Blueprint ID
 * 1 = Ore-collecting robot ore cost
 * 2 = Clay-collecting robot ore cost
 * 3 = Obsidian-collecting robot ore cost
 * 4 = Obsidian-collecting robot clay cost
 * 5 = Geode-cracking robot ore cost
 * 6 = Geode-cracking robot obsidian cost
 *
 * Indices 3 and 4 are needed to make an obsidian-collecting robot
 * Indices 5 and 6 are needed to make a geode-cracking robot
 */
func parseInput(fileName string) [][]int {
	data, error := os.ReadFile(fileName)
	if error != nil {
		fmt.Println(error.Error())
		os.Exit(1)
	}

	// Convert the byte array (as a slice) into a long string
	// Note that Go cannot be directly turned into a string, but slices can
	dataStr := string(data[:])

	var blueprints [][]int // Declare it

	bpLines := strings.Split(dataStr, "\n")
	r := regexp.MustCompile("[0-9]+")
	for i := 0; i < len(bpLines); i++ {
		line := bpLines[i]
		matches := r.FindAllString(line, -1)

		if matches == nil {
			fmt.Printf("Error parsing input file %s.\n", fileName)
			os.Exit(1)
		}

		// Not the prettiest way to write it
		var blueprint []int
		for m := 0; m < len(matches); m++ {
			val, _ := strconv.Atoi(matches[m])
			blueprint = append(blueprint, val)
		}

		blueprints = append(blueprints, blueprint)
	}

	return blueprints // Return it
}

/**
 * Helper function to check if we can actually construct a specific type of
 * robot. Returns true if we can, false otherwise. Basically just parses
 * the 32-bit int of rocks into the blueprint robot costs.
 */
func canConstruct(index int, blueprint []int, rocks uint32) bool {
	// The mapping goes:
	// index 0 -> blueprint[1] and rocks[0]
	// index 1 -> blueprint[2] and rocks[0]
	// index 2 -> blueprint[3] and rocks[0] with blueprint[4] and rocks[1]
	// index 3 -> blueprint[5] and rocks[0] with blueprint[6] and rocks[2]
	if index == 0 { // Ore robot
		return getOre(rocks) >= blueprint[1]
	}
	if index == 1 { // Clay robot
		return getOre(rocks) >= blueprint[2]
	}
	if index == 2 { // Obsidian robot
		return getOre(rocks) >= blueprint[3] && getClay(rocks) >= blueprint[4]
	}
	if index == 3 { // Geode robot
		return getOre(rocks) >= blueprint[5] && getObsidian(rocks) >= blueprint[6]
	}
	// Default case; should never happen
	return false
}

/**
 * Helper function to actually decrement the rocks by the cost
 * of the robot.
 */
func consumeRocks(index int, blueprint []int, rocks uint32) uint32 {
	var val uint32
	if index == 0 { // Ore robot
		val = uint32(blueprint[1])
	}
	if index == 1 { // Clay robot
		val = uint32(blueprint[2])
	}
	if index == 2 { // Obsidian robot
		val = uint32(blueprint[3]) + (uint32(blueprint[4]) << 8)
	}
	if index == 3 { // Geode robot
		val = uint32(blueprint[5]) + (uint32(blueprint[6]) << 16)
	}
	return (rocks - val)
}

/**
 * Recursive function to run through all possible iterations of the robot creation and mining operation.
 */
func runRecurse(bp []int, robots uint32, rocks uint32, nextRobot int, max *int, minutes int) {
	// First we need all the robots to collect ore
	newRocks := rocks + robots

	// Now add the newly constructed robot to the roster at the end of the minute
	newRobots := robots
	if nextRobot != -1 {
		newRobots += 0x01 << (8 * nextRobot)
	}

	// Base case: we've run out of minutes, so count up the geodes and calculate the quality level
	if minutes == 1 {
		id := bp[0]
		geodes := getGeodes(newRocks)
		if id*geodes > *max {
			*max = id * geodes
		}
	} else {
		// Now go through and recurse on each type of robot you can create
		// Always try to create the most important robot...
		if canConstruct(3, bp, newRocks) {
			runRecurse(bp, newRobots, consumeRocks(3, bp, newRocks), 3, max, minutes-1)
		} else if canConstruct(2, bp, newRocks) {
			runRecurse(bp, newRobots, consumeRocks(2, bp, newRocks), 2, max, minutes-1)
		} else if canConstruct(1, bp, newRocks) {
			runRecurse(bp, newRobots, consumeRocks(1, bp, newRocks), 1, max, minutes-1)
		}
		if canConstruct(0, bp, newRocks) {
			runRecurse(bp, newRobots, consumeRocks(0, bp, newRocks), 0, max, minutes-1)
		}
		runRecurse(bp, newRobots, newRocks, -1, max, minutes-1)
	}
}

func getOre(rocks uint32) int {
	return int(rocks & 0xFF)
}

func getClay(rocks uint32) int {
	return int((rocks >> 8) & 0xFF)
}

func getObsidian(rocks uint32) int {
	return int((rocks >> 16) & 0xFF)
}

func getGeodes(rocks uint32) int {
	return int((rocks >> 24) & 0xFF)
}

/**
 * Kicks off the recursive algorithm with initial values.
 */
func runBlueprint(bp []int) int {
	var robots uint32
	robots = 0x00000001
	var rocks uint32
	rocks = 0x00000000 // Always starts at 0
	max := 0

	runRecurse(bp, robots, rocks, -1, &max, 24)

	return max
}

/**
 * The main script being run here. Parses the input and outputs the solution value.
 */
func main() {
	// Step 1: Read the input file, parse it into Blueprints
	inputFile := "input.txt"
	if len(os.Args) == 2 && os.Args[1] == "-sample" {
		inputFile = "sample_input.txt"
	}
	blueprints := parseInput(inputFile)

	// Now go through each blueprint and create a run!
	sum := 0
	for b := 0; b < len(blueprints); b++ {
		runVal := runBlueprint(blueprints[b])
		fmt.Printf("BP#%d gets %d geodes\n", b+1, runVal)
		sum += runVal
	}

	fmt.Printf("Part 1: %d\n", sum)
}
