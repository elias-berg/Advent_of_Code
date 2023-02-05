#include <string>
#include <map>

using namespace std;

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

    void Add(char dir, Tile* t);
    Tile* GetNext(char dir);
    Tile* GetNextSpace(char dir);

  private:
    int X;
    int Y;
    TileType Type; 
    map<char, Tile*> Adj;
};