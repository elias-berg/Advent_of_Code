#include <map>

#include "Tile.h"

using namespace std;

Tile::Tile() {
  X = -1;
  Y = -1;
}

Tile::Tile(int x, int y, char c) {
  X = x;
  Y = y;
  if (c == '#') {
    Type = WALL;
  } else {
    Type = SPACE;
  }
}

int Tile::GetX() {
  return X;
}

int Tile::GetY() {
  return Y;
}

TileType Tile::GetType() {
  return Type;
}

void Tile::Add(char dir, Tile* t) {
  Adj[dir] = t;
}

Tile* Tile::GetNextSpace(char dir) {
  Tile* next = GetNext(dir);
  if (next == NULL) {
    return NULL;
  }
  // If we come up to a wall, then don't proceed past it
  if (next->Type == WALL) {
    return this;
  }
  return next;
}

Tile* Tile::GetNext(char dir) {
  Tile* next = NULL;
  try {
    next = Adj.at(dir);
  } catch (out_of_range &oor) {
    next = NULL;
  }
  return next;
}