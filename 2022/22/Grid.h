#ifndef GRID_H
#define GRID_H

#include <string>
#include <map>

#include "Tile.h"
#include "Container.h"

class Grid : Container {
  public:
    Tile* ParseLine(int y, std::string line);
    Tile* GetNextSpace(char* facing, int x, int y);
    Tile* GetTile(int x, int y);

  protected:
    std::map<std::string, Tile*> grid;
};

#endif // GRID_H