#ifndef CONTAINER_H
#define CONTAINER_H

#include <string>

#include "Tile.h"

class Container {
  public:
    virtual Tile* ParseLine(int y, std::string line) = 0;
    virtual Tile* GetNextSpace(char* facing, int x, int y) = 0;
    inline std::string ToKey(int x, int y) {
      return std::to_string(x) + "," + std::to_string(y);
    };
};

#endif