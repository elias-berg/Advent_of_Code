// Advent of Code 2022 - Day 22
// Monkey Map
//
// The monkeys guide you up to a force field protecting the grove
// the elves should be in. The force field has a password that involves
// tracing a shape on an input device. The input device is a series of
// "spaces" and "walls", where you can trace along spaces but can't trace
// through walls. The spaces also wrap around to the other side if tracing
// past an edge. The second part of the input is the series of movements
// where a number is the number of spaces to move in the current direction
// and characters are either 'L' or 'R' and dictate a counter-clockwise
// or clockwise rotation, respectively.
//
// Part 1 -
// What is the value of the final position given that you start at the
// top-left-most position in the map and the series of inputs, where
// value = (1000 * Y-position) + (4 * X-position) + final direction?
// Note that final direction is 0 for right, 1 for down, 2 for left,
// and 3 for up.

// Use the following commands to run:
// - `g++ *.cpp`
// - `./a.out`

#include <iostream>
#include <fstream>
#include <strstream>
#include <string>
#include <map>

#include "Tile.h"
#include "Grid.h"
#include "Cube.h"

using namespace std;

char turn(char facing, char dir) {
  if (facing == '>') {
    return dir == 'R' ? 'v' : '^';
  } else if (facing == 'v') {
    return dir == 'R' ? '<' : '>';
  } else if (facing == '<') {
    return dir == 'R' ? '^' : 'v';
  } else { // Assuming it MUST be '^'
    return dir == 'R' ? '>' : '<';
  }
}

int faceValue(char facing) {
  switch (facing) {
    case '>':
      return 0;
    case 'v':
      return 1;
    case '<':
      return 2;
    default: // Assumption this is '^'
      return 3;
  }
}

void part1(Grid* grid, Tile* curTile, string sequence) {
  char facing = '>'; // We always start facing right
  int dist;
  char turnDir;
  std::istrstream sequenceStream(sequence.data());
  while (!sequenceStream.eof()) {
    // Move the specified distance
    sequenceStream >> dist;
    for (int i = 0; i < dist; i++) {
      int x = curTile->GetX();
      int y = curTile->GetY();
      Tile* nextTile = grid->GetNextSpace(facing, x, y);
      // If we hit a wall, then skip moving any further
      if (curTile == nextTile) {
        break;
      } else {
        curTile = nextTile;
      }
    }

    // Turn (keeping in mind that the last thing we read in should be a move)
    if (!sequenceStream.eof()) {
      sequenceStream >> turnDir;
      facing = turn(facing, turnDir);
    }
  }

  std::cout << "Part 1: " << (1000 * curTile->GetY()) + (4 * curTile->GetX()) + faceValue(facing) << "\n";
}

void part2(Cube* cube, Tile* curTile, string sequence) {
  char facing = '>'; // We always start facing right
  int dist;
  char turnDir;
  std::istrstream sequenceStream(sequence.data());
  while (!sequenceStream.eof()) {
    // Move the specified distance
    sequenceStream >> dist;
    for (int i = 0; i < dist; i++) {
      int x = curTile->GetX();
      int y = curTile->GetY();
      Tile* nextTile = cube->GetNextSpace(&facing, x, y); // The facing direction may change!
      // If we hit a wall, then skip moving any further
      if (curTile == nextTile) {
        break;
      } else {
        curTile = nextTile;
      }
    }

    // Turn (keeping in mind that the last thing we read in should be a move)
    if (!sequenceStream.eof()) {
      sequenceStream >> turnDir;
      facing = turn(facing, turnDir);
    }
  }

  std::cout << "Part 2: " << (1000 * curTile->GetY()) + (4 * curTile->GetX()) + faceValue(facing) << "\n";
}

int main(int argc, char** argv) {
  string fileName = "input.txt";
  int faceSize = 50; // Part 2 face size for the cube
  if (argc == 2 && strcmp(argv[1], "-sample") == 0) {
    fileName = "sample_input.txt";
    faceSize = 4; // Sample has 4x4 faces
  }

  ifstream f;
  f.open(fileName);

  Grid* grid = new Grid(); // Part 1
  Cube* cube = new Cube(faceSize); // Part 2

  Tile* part1Start = NULL;
  Tile* part2Start = NULL;
  int y = 1;

  // Parse the input into 
  string line;
  std::getline(f, line);
  Tile* firstOfRow = NULL;
  while (strcmp(line.data(), "") != 0) {
    // Part 1 - Grid construction
    firstOfRow = grid->ParseLine(y, line);
    if (part1Start == NULL) {
      part1Start = firstOfRow;
    }
    // Part 2 - Cube construction
    firstOfRow = cube->ParseLine(y, line);
    if (part2Start == NULL) {
      part2Start = firstOfRow;
    }

    y++; // The max Y position is just whatever the last line is (origin is 1,1)
    std::getline(f, line);
  }

  // Debug the cube
  cube->ConstructCube();

  // Now get the sequence to follow
  string sequence;
  std::getline(f, sequence);
  f.close();

  // Off to the races!
  part1(grid, part1Start, sequence);

  //part2()
  // Should probably clean up the memory here
}