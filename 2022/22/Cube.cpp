#include <iostream>
#include <map>
#include <queue>
#include <string>
#include <cmath>

#include "Tile.h"
#include "Grid.h"
#include "Vertex.h"
#include "Cube.h"

using namespace std;

#define DEBUG false

/////////////////
// CubeFace Class
/////////////////

string CubeFace::ToString() {
  return to_string(X) + "," + to_string(Y);
}
// Generically adds a tile to the grid "map"
void CubeFace::AddTile(string key, Tile* t) {
  grid[key] = t;
}

// Simple helper function to see if a CubeFace has any other
// particular CubeFace as a neighbor. For constructing the cube.
bool CubeFace::HasNeighbor(CubeFace* neighbor) {
  try {
    char dir = Neighbor2Side.at(neighbor);
    return dir == '>' || dir == '<' || dir == 'v' || dir == '^';
  } catch (out_of_range &oor) {
    return false;
  }
}

// When constructing a cube face, we want to set its vertices and all of the
// directions the vertices are facing so when we rotate each face of the cube
// to actually make the cube, we can determine the direction each neighbor is
// facing due to the rotation of the vertices.
// Note that the vertices will undergo a transformation!
CubeFace::CubeFace(int x, int y) {
  X = x;
  Y = y;
  Flipped = false;

  Vertices = new Vertex*[4];
  Vertices[0] = new Vertex(x, y, 0); // Always in the top-left
  Vertices[1] = new Vertex(x + 1, y, 0); // Top-right
  Vertices[2] = new Vertex(x, y + 1, 0); // Bottom-left
  Vertices[3] = new Vertex(x + 1, y + 1, 0); // Bottom-right

  AdjCnt = 0;
  Neighbors = new CubeFace*[4]; // Max of 4!

  // Now set the pairs!
  Side2Vertices['^'] = new VertexPair(Vertices[0], Vertices[1]);
  Side2Vertices['v'] = new VertexPair(Vertices[2], Vertices[3]);
  Side2Vertices['<'] = new VertexPair(Vertices[0], Vertices[2]);
  Side2Vertices['>'] = new VertexPair(Vertices[1], Vertices[3]);
}

/////////////
// Cube Class
/////////////

Cube::Cube(int faceSize) {
  FaceSize = faceSize;
  FaceCnt = 0;
  Faces = new CubeFace*[6];
}

CubeFace* Cube::GetFace(int quadX, int quadY) {
  CubeFace* cf = NULL;
  try {
    string key = ToKey(quadX, quadY);
    cf = FaceByCoord.at(key);
  } catch (out_of_range &oor) {
    cf = NULL;
  }
  return cf;
}

Tile* Cube::GetTile(int x, int y) {
  int quadX = (x-1) / FaceSize;
  int quadY = (y-1) / FaceSize;
  CubeFace* face = GetFace(quadX, quadY);
  if (face != NULL) {
    return face->GetTile(x, y);
  }
  return NULL;
}

// Much like the Grid::ParseLine, the difference is that we determine what
// cube face the tile belongs to, create the face if needed, and then
// add the relative tile position to the face
Tile* Cube::ParseLine(int y, string line) {
  Tile *first = NULL, *next;
  for (int i = 0; i < line.length(); i++) {
    char cur = line[i];
    int x = i + 1; // Since the origin is 1,1

    if (cur != ' ') {
      // First get the face that this Tile belongs to
      int quadX = (x-1) / FaceSize;
      int quadY = (y-1) / FaceSize;

      CubeFace* face = GetFace(quadX, quadY);
      if (face == NULL) {
        face = new CubeFace(quadX, quadY);
        string quadKey = ToKey(quadX, quadY);
        FaceByCoord[quadKey] = face;

        Faces[FaceCnt] = face;
        FaceCnt++;
      }

      // Now add the tile to the face
      next = new Tile(x, y, cur);
      string key = ToKey(x, y);
      face->AddTile(key, next);

      // Set the first tile
      if (first == NULL) {
        first = next;
      }
    }
  }

  return first;
}

// Given a face direction, return the opposite direction.
// Used when moving faces of the cube, need to actually face the opposite
// direction of the direction the previous face is relative to the new face.
char Opposite(char facing) {
  if (facing == '^') {
    return 'v';
  } else if (facing == 'v') {
    return '^';
  } else if (facing == '>') {
    return '<';
  } else { // facing == '<'
    return '>';
  }
}

// This function takes the direction we moved from the previous face (prevDir), the direction the previous
// face is facing relative to the new face we're moving onto (nextDir), that next face, and the last tile's
// x and y coordinates on the flat cube to determine the corresponding coordinates on the "nextFace" that
// we'll end up at.
//
// Fun fact, I drew all of the possible face combinations to come up with the if-block structure. It was
// not a lot of fun...
Tile* Cube::FlipCoordinates(char prevDir, char nextDir, CubeFace* nextFace, int oldX, int oldY, int faceSize) {
  int x = oldX % faceSize;
  int y = oldY % faceSize;
  if (x == 0) { x = faceSize; }
  if (y == 0) { y = faceSize; }
  // Here comes the fun flipping logic. Depending on which direction we cross over
  // and what side of the new face we land on will determine the new coordinates.
  int newX, newY;
  if (prevDir == '>') { // Went off in the +X direction
    if (nextDir == '<') { // Natural neighbor
      newX = 1;
      newY = y;
    } else if (nextDir == '^') { // 90deg counter-clockwise
      newX = (faceSize - y) + 1;
      newY = 1;
    } else if (nextDir == 'v') { // 90deg clockwise
      newX = y;
      newY = faceSize;
    } else { // nextDir == '>'
      newX = faceSize;
      newY = (faceSize - y) + 1;
    }
  } else if (prevDir == 'v') { // Went off in the +Y direction
    if (nextDir == '^') { // Natural neighbor
      newX = x;
      newY = 1;
    } else if (nextDir == '>') { // CC
      newX = faceSize;
      newY = x;
    } else if (nextDir == '<') { // C
      newX = 1;
      newY = (faceSize - x) + 1;
    } else { // nextDir == 'v'
      newX = (faceSize - x) + 1;
      newY = faceSize;
    }
  } else if (prevDir == '^') { // Went off in the -Y direction
    if (nextDir == 'v') { // Natural neighbor
      newX = x;
      newY = faceSize;
    } else if (nextDir == '<') { // CC
      newX = 1;
      newY = x;
    } else if (nextDir == '>') { // C
      newX = faceSize;
      newY = (faceSize - x) + 1;
    } else { // nextDir == '^'
      newX = (faceSize - x) + 1;
      newY = 1;
    }
  } else { // prevDir == '<'; // Went off in the -X direction
    if (nextDir == '>') { // Natural neighbor
      newX = faceSize;
      newY = y;
    } else if (nextDir == 'v') { // CC
      newX = (faceSize - y) + 1;
      newY = faceSize;
    } else if (nextDir == '^') { // C
      newX = y;
      newY = 1;
    } else { // nextDir == '<'
      newX = 1;
      newY = (faceSize - y) + 1;
    }
  }

  // Now get the face-relative position and get the tile!
  x = (nextFace->X * faceSize) + newX;
  y = (nextFace->Y * faceSize) + newY;
  return GetTile(x, y);
}

Tile* Cube::GetNextSpace(char* facing, int x, int y) {
  int xMod = 0;
  int yMod = 0;
  if (*facing == '>') {
    xMod = 1;
  } else if (*facing == '<') {
    xMod = -1;
  } else if (*facing == 'v') {
    yMod = 1;
  } else { // *facing == '^'
    yMod = -1;
  }

  Tile* nextTile = GetTile(x + xMod, y + yMod);

  // Return self if the next tile is actually a wall
  if (nextTile != NULL && nextTile->GetType() == WALL) {
    return GetTile(x, y);
  }

  // Else, we need to move onto another cube face
  if (nextTile == NULL) {
    int quadX = (x-1) / FaceSize;
    int quadY = (y-1) / FaceSize;
    string quadKey = ToKey(quadX, quadY);
    CubeFace* face = FaceByCoord[quadKey];

    CubeFace* nextFace;
    if (xMod == 1) { // To the right
      nextFace = face->Side2Neighbor['>'];
    } else if (xMod == -1) {
      nextFace = face->Side2Neighbor['<'];
    } else if (yMod == 1) {
      nextFace = face->Side2Neighbor['v'];
    } else { // yMod == -1
      nextFace = face->Side2Neighbor['^'];
    }
    // If we go up, but it's the right side of the next face, then
    // we need to face left.
    char nextDir = nextFace->Neighbor2Side[face];
    nextTile = FlipCoordinates(*facing, nextDir, nextFace, x, y, FaceSize);

    if (nextTile->GetType() == WALL) {
      return GetTile(x, y);
    }

    // Don't forget to update the direction we're facing
    *facing = Opposite(nextDir);
  }

  return nextTile;
}

// Helper function to set two cube faces as neighbors to each other
void SetNeighbors(CubeFace* a, char bDir, CubeFace* b, char aDir) {
  a->Neighbor2Side[b] = bDir;
  a->Side2Neighbor[bDir] = b;
  b->Neighbor2Side[a] = aDir;
  b->Side2Neighbor[aDir] = a;

  a->Neighbors[a->AdjCnt] = b;
  a->AdjCnt++;

  b->Neighbors[b->AdjCnt] = a;
  b->AdjCnt++;
}

// Helper function to return a 2-sized array of vertices shared between two faces
Vertex** GetSharedVertices(CubeFace* a, CubeFace* b) {
  int sharedCnt = 0;
  Vertex** shared = new Vertex*[2];

  Vertex** aV = a->Vertices;
  Vertex** bV = b->Vertices;
  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 4; j++) {
      if (aV[i]->equals(bV[j])) {
        shared[sharedCnt] = aV[i];
        sharedCnt++;

        if (sharedCnt == 2) {
          return shared;
        }
      }
    }
  }

  delete[] shared;
  return NULL; // Weird sanity check -> should cause problems
}

void RotateAllVertices(CubeFace* prev, CubeFace* face, char axis, int dir, int x, int y, int z) {
  // Rotate the current first...
  for (int i = 0; i < 4; i++) {
    face->Vertices[i]->Rotate(axis, dir, x, y, z);
  }

  // Then move on to rotate all of the subsequent, previously flipped faces
  map<CubeFace*, bool> visited;
  visited[prev] = true;
  visited[face] = true;

  queue<CubeFace*> Q;
  Q.push(face);

  while (Q.size() > 0) {
    CubeFace* cur = Q.front();
    Q.pop();

    for (int n = 0; n < cur->AdjCnt; n++) {
      CubeFace* neigh = cur->Neighbors[n];
      if (neigh->Flipped && !visited[neigh]) {
        Q.push(neigh);
        visited[neigh] = true;
        for (int i = 0; i < 4; i++) {
          neigh->Vertices[i]->Rotate(axis, dir, x, y, z);
        }
      }
    }
  }
}

// Rotate the 'b' face 90 degrees relative to the 'a' face.
// This means: find the axis that they have in common and rotate over it.
// I.e. we find the two vertices that the faces have in common, then
// find the axis that changes value between both of those vertices.
// E.g. (1,1,1) and (1,0,1) only differs on the y-axis, so we need
// to rotate all of the points around the y-axis
void Cube::RotateFace3D(CubeFace* a, CubeFace* b) {
  Vertex** shared = GetSharedVertices(a, b);
  // Now we find out what axis has different values and we rotate over that axis.
  Vertex* v1 = shared[0];
  Vertex* v2 = shared[1];
  int dir = 1;
  char bIsTo = a->Neighbor2Side.at(b);
  if (bIsTo == '<' || bIsTo == 'v') {
    dir = -1;
  }
  
  if (v1->X != v2->X) {
    RotateAllVertices(a, b, 'x', dir, 0, v1->Y, v1->Z);
  } else if (v1->Y != v2->Y) {
    RotateAllVertices(a, b, 'y', dir, v1->X, 0, v1->Z);
  } else { // Rotate over z-axis
    RotateAllVertices(a, b, 'z', dir, v1->X, v1->Y, 0);
  }

  delete[] shared; // Clean up, eh?
}

void Cube::FlipFacesRecursive(CubeFace* prev, CubeFace* cur) {
  // Base case: we're at a leaf
  if (cur->AdjCnt == 1) {
    RotateFace3D(prev, cur);
  } else {
    for (int i = 0; i < cur->AdjCnt; i++) {
      CubeFace* next = cur->Neighbors[i];
      // Only recurse on nodes we haven't previously flipped
      if (!next->Flipped && next != prev) {
        FlipFacesRecursive(cur, next);
      }
    }
    RotateFace3D(prev, cur);
  }
  cur->Flipped = true;
}

// Face-flipping logic:
// - Start with 1 -> recurse down to a leaf.
// -- Flip the leaf relative to its non-leaf neighbor
// -- Flip the non-leaf neighbor
// -- Eventually we'll make out way back to 1 and its neighbors will have
//    flipped relative to itself.
void Cube::FlipFaces() {
  // Populate the 'visited' collection
  CubeFace* cur = Faces[0];
  cur->Flipped = true;
  for (int i = 0; i < cur->AdjCnt; i++) {
    FlipFacesRecursive(cur, cur->Neighbors[i]);
  }
}

// Goes through each point of the faces to determine if the faces
// are neighbors.
void CheckNeighbors2D(CubeFace* a, CubeFace* b) {
  Vertex** shared = GetSharedVertices(a, b);
  // No matches!
  if (shared == NULL) {
    return;
  }
  // If we have two shared vertices, then now we need to find out what axis they reside on
  if (shared[0]->X == shared[1]->X) { // Xs are equal -> vertical edge (left/right neighbors)
    if (a->X < b->X) { // a is to the right of b
      SetNeighbors(a, '>', b, '<');
    } else { // b is to the right of a
      SetNeighbors(a, '<', b, '>');
    }
  } else { // Assuming here that the Ys are equal now -> horizontal edge (up/down neighbors)
    if (a->Y > b->Y) { // a above b
      SetNeighbors(a, '^', b, 'v');
    } else { // a below b
      SetNeighbors(a, 'v', b, '^');
    }
  }
  delete[] shared;
}

char GetVertexDirection(Vertex* v1, Vertex* v2, CubeFace* face) {
  VertexPair* pair = new VertexPair(v1, v2);
  char dir[] = "<>^v";
  for (int i = 0; i < 4; i++) {
    VertexPair* vp = face->Side2Vertices[dir[i]];
    if (vp->equals(pair)) {
      delete pair;
      return dir[i];
    }
  }
  delete pair;
  return -1;
}

void CheckNeighbors3D(CubeFace* a, CubeFace* b) {
  Vertex** shared = GetSharedVertices(a, b);
  // No matches!
  if (shared == NULL) {
    return;
  }
  // Now, we need to get the direction the shared vertices are
  // for the original faces
  Vertex* v1 = shared[0];
  Vertex* v2 = shared[1];

  char bDir = GetVertexDirection(v1, v2, a);
  char aDir = GetVertexDirection(v1, v2, b);
  if (aDir != -1 && bDir != -1) {
    SetNeighbors(a, bDir, b, aDir);
  }

  delete[] shared;
}

void Cube::ConstructCube() {
  // First, go through all possible faces and map them out to each other
  for (int f = 0; f < FaceCnt; f++) {
    CubeFace* curFace = Faces[f];
    // Now iterate through all other faces and find neighbors
    for (int o = 0; o < FaceCnt; o++) {
      if (o != f) {
        CubeFace* otherFace = Faces[o];
        if (!otherFace->HasNeighbor(curFace)) {
          CheckNeighbors2D(curFace, otherFace);
        }
      }
    }
  }

  // Now that we have the flattened neighbors, we need to do a BFS and flip each
  // neighbor 90deg clockwise.
  FlipFaces();

  // Now that we have our cube, we need to go back through and find all the NEW edge
  // directions
  for (int f = 0; f < FaceCnt; f++) {
    CubeFace* curFace = Faces[f];
    // Now iterate through all other faces and find neighbors
    for (int o = 0; o < FaceCnt; o++) {
      if (o != f) {
        CubeFace* otherFace = Faces[o];
        if (!otherFace->HasNeighbor(curFace)) {
          CheckNeighbors3D(curFace, otherFace);
        }
      }
    }
  }

  #if DEBUG
  PrintAllNeighbors();
  #endif
}

// Debugging helper function
void Cube::PrintAllVertices(bool unique) {
  std::map<std::string, bool> uniqueVs;

  for (int f = 0; f < FaceCnt; f++) {
    CubeFace* face = Faces[f];
    Vertex** vertices = face->Vertices;
    if (!unique) {
      cout << "Face " << face->X << "," << face->Y << ":\n";
    }
    for (int i = 0; i < 4; i++) {
      Vertex* v = vertices[i];
      string key = std::to_string(v->X) + std::to_string(v->Y) + std::to_string(v->Z);
      if (unique && !uniqueVs[key]) {
        cout << v->ToString() << "\n";
        uniqueVs[key] = true;
      } else if (!unique) {
        cout << v->ToString() << "\n";
      }
    }
  }
}

// Debugging helper function
void Cube::PrintAllNeighbors() {
  char dir[] = "<>^v";

  for (int f = 0; f < FaceCnt; f++) {
    CubeFace* face = Faces[f];
    cout << "Cube Face " << face->ToString() << ":\n";
    for (int i = 0; i < 4; i++) {
      VertexPair* vp = face->Side2Vertices[dir[i]];
      Vertex* a = vp->A;
      Vertex* b = vp->B;

      string keyA = a->ToString();
      string keyB = b->ToString();
      CubeFace* n = face->Side2Neighbor[dir[i]];
      cout << "Side " << keyA << " and " << keyB << " " << dir[i] << " " << n->X << "," << n->Y << "\n";
    }
  }
}