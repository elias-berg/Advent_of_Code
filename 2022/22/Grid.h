#ifndef GRID_H
#define GRID_H

#include <string>
#include <map>

#include "Tile.h"

class Grid {
  public:
    Tile* ParseLine(int y, std::string line);
    Tile* GetNextSpace(char facing, int x, int y);

  protected:
    std::string ToKey(int x, int y);
    Tile* GetTile(int x, int y);

    std::map<std::string, Tile*> grid;
};

#endif // GRID_H