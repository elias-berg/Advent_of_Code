#include <map>
#include <string>

#include "Grid.h"

using namespace std;

Tile* Grid::GetTile(int x, int y) {
  Tile* t = NULL;
  try {
    string key = ToKey(x, y);
    t = grid.at(key);
  } catch (out_of_range &oor) {
    t = NULL;
  }
  return t;
}

// Parses a string of spaces and walls into Tiles, stuffs
// them in the grid, then returns the first tile of the row.
Tile* Grid::ParseLine(int y, string line) {
  Tile *first = NULL, *next;
  for (int i = 0; i < line.length(); i++) {
    char cur = line[i];
    int x = i + 1; // Since the origin is 1,1

    if (cur != ' ') {
      next = new Tile(x, y, cur);
      string key = ToKey(x, y);
      grid[key] = next;

      // Set the first tile
      if (first == NULL) {
        first = next;
      }
    }
  }

  return first;
}

Tile* Grid::GetNextSpace(char* facing, int x, int y) {
  int xMod = 0;
  int yMod = 0;
  Tile* nextTile = NULL;
  switch (*facing) {
    case '>':
      xMod = -1;
      nextTile = GetTile(x+1, y);
      break;
    case 'v':
      yMod = -1;
      nextTile = GetTile(x, y+1);
      break;
    case '<':
      xMod = 1;
      nextTile = GetTile(x-1, y);
      break;
    default: // '^'
      yMod = 1;
      nextTile = GetTile(x, y-1);
      break;
  }
  // Return self if the next tile is actually a wall
  if (nextTile != NULL && nextTile->GetType() == WALL) {
    return GetTile(x, y);
  }
  // Else, we hit an edge and need to wrap around
  if (nextTile == NULL) {
    int newX = x + xMod;
    int newY = y + yMod;
    Tile* wrappedTile = GetTile(newX, newY);
    while (wrappedTile != NULL) {
      nextTile = wrappedTile;
      newX += xMod;
      newY += yMod;
      wrappedTile = GetTile(newX, newY);
    }
    if (nextTile->GetType() == WALL) {
      return GetTile(x, y);
    }
  }
  return nextTile;
}