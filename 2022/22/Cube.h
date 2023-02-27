#ifndef CUBE_H
#define CUBE_H

#include <map>
#include <string>

#include "Tile.h"
#include "Grid.h"
#include "Vertex.h"
#include "Container.h"

class CubeFace : public Grid {
  public:
    int X;
    int Y;
    Vertex** Vertices;
    // Constructor to create a cube face at a 2D position.
    // Note that x and y are the top-left vertex coordinates.
    CubeFace(int x, int y);
    void AddTile(std::string key, Tile* t);

    int AdjCnt;
    CubeFace** Neighbors; // Collection of all adjacent faces
    bool HasNeighbor(CubeFace* neighbor);

    bool Flipped;

    // Each face has a reference to the other faces that touch
    // each edge. We have an edge->face dictionary for iterating
    // across each neighbor and determining which neighbor we
    // go to when crossing that edge. The face->edge map is then
    // for when we get the face we're crossing over to to get
    // the direction we should be facing.
    std::map<char, CubeFace*> Side2Neighbor;
    std::map<CubeFace*, char> Neighbor2Side;
    std::map<char, VertexPair*> Side2Vertices;
    std::string ToString();
};

class Cube : Container {
  public:
    Cube(int faceSize);
    Tile* ParseLine(int y, std::string line);
    Tile* GetNextSpace(char* facing, int x, int y);
    // This function is important to call once all lines are parsed in
    // order to appropriately:
    // - Map all neighboring faces
    // - Flip all vertices
    // - Link the faces together via cube edges
    void ConstructCube();
    Tile* GetTile(int x, int y);
    Tile* FlipCoordinates(char prevDir, char nextDir, CubeFace* nextFace, int oldX, int oldY, int faceSize);

  private:
    int FaceSize; // Determines what Face a Tile belongs to

    int FaceCnt; // For making sure we hit 6
    CubeFace** Faces; // Collection of all faces
    void FlipFaces();
    void FlipFacesRecursive(CubeFace* adj, CubeFace* cur);
    void RotateFace3D(CubeFace* a, CubeFace* b);

    // Map-related data
    // The cube is effectively just a size-6 collection
    // of Grid faces, each being 50x50 tiles
    CubeFace* GetFace(int x, int y);
    // Coordinate string -> CubeFace
    std::map<std::string, CubeFace*> FaceByCoord;
    
    // For debugging
    void PrintAllVertices(bool unique);
    void PrintAllNeighbors();
};

#endif