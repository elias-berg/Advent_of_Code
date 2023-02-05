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

using namespace std;

string toKey(int x, int y) {
  return std::to_string(x) + "," + std::to_string(y);
}

Tile* getMappedTile(map<string, Tile*>* grid, int x, int y) {
  Tile* t = NULL;
  try {
    t = grid->at(toKey(x, y));
  } catch (out_of_range &oor) {
    t = NULL;
  }
  return t;
}

Tile* line2Tiles(map<string, Tile*>* grid, int y, string line) {
  Tile *first = NULL, *next;
  for (int i = 0; i < line.length(); i++) {
    char cur = line[i];
    int x = i + 1; // Since the origin is 1,1

    if (cur != ' ') {
      next = new Tile(x, y, cur);
      (*grid)[toKey(x, y)] = next;

      // Set the first tile
      if (first == NULL) {
        first = next;
      }
    }
  }

  return first;
}

/**
 * There's surely a much better way to write this, but I don't really have the
 * mental capacity to even bother since I'm relearning C++ as-is.
 */
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

Tile* getNextSpace(map<string, Tile*>* grid, char facing, int x, int y) {
  int xMod = 0;
  int yMod = 0;
  Tile* nextTile = NULL;
  switch (facing) {
    case '>':
      xMod = -1;
      nextTile = getMappedTile(grid, x+1, y);
      break;
    case 'v':
      yMod = -1;
      nextTile = getMappedTile(grid, x, y+1);
      break;
    case '<':
      xMod = 1;
      nextTile = getMappedTile(grid, x-1, y);
      break;
    default: // '^'
      yMod = 1;
      nextTile = getMappedTile(grid, x, y-1);
      break;
  }
  // Return self if the next tile is actually a wall
  if (nextTile != NULL && nextTile->GetType() == WALL) {
    return getMappedTile(grid, x, y);
  }
  // Else, we hit an edge and need to wrap around
  if (nextTile == NULL) {
    int newX = x + xMod;
    int newY = y + yMod;
    Tile* wrappedTile = getMappedTile(grid, newX, newY);
    while (wrappedTile != NULL) {
      nextTile = wrappedTile;
      newX += xMod;
      newY += yMod;
      wrappedTile = getMappedTile(grid, newX, newY);
    }
    if (nextTile->GetType() == WALL) {
      return getMappedTile(grid, x, y);
    }
  }
  return nextTile;
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

int main(int argc, char** argv) {
  string fileName = "input.txt";
  if (argc == 2 && strcmp(argv[1], "-sample") == 0) {
    fileName = "sample_input.txt";
  }

  ifstream f;
  f.open(fileName);

  Tile* curTile = NULL;
  map<string, Tile*> grid;
  int y = 1;

  // Parse the input into 
  string line;
  std::getline(f, line);
  Tile* firstOfRow = NULL;
  while (strcmp(line.data(), "") != 0) {
    firstOfRow = line2Tiles(&grid, y, line);
    if (curTile == NULL) {
      curTile = firstOfRow;
    }
    y++; // The max Y position is just whatever the last line is (origin is 1,1)
    std::getline(f, line);
  }

  // Now get the sequence to follow
  string sequence;
  std::getline(f, sequence);
  f.close();

  // Off to the races!
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
      Tile* nextTile = getNextSpace(&grid, facing, x, y);
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

  // Should probably clean up the memory here
}