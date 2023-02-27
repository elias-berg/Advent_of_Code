#ifndef TILE_H
#define TILE_H

enum TileType {
  SPACE,
  WALL
};

class Tile {
  public:
    Tile();
    Tile(int x, int y, char c);
    
    int GetX();
    int GetY();
    TileType GetType();

  private:
    int X;
    int Y;
    TileType Type;
};

#endif