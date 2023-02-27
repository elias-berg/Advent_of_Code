#include "Tile.h"

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