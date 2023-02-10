#include <iostream>
#include <map>
#include <queue>
#include <string>
#include <cmath>

#include "Tile.h"
#include "Grid.h"
#include "Cube.h"

using namespace std;

#define DEBUG true

Vertex::Vertex(int x, int y, int z) {
  X = x;
  Y = y;
  Z = z;
}

void Vertex::PrintVertex() {
  std::cout << "(" << X << "," << Y << "," << Z << ")\n";
}

bool Vertex::equals(Vertex* rhs)  {
  return X == rhs->X && Y == rhs->Y && Z == rhs->Z;
}

// Wrapper around a pair of vertices to make it easy to later map edge directions
VertexPair::VertexPair(Vertex* a, Vertex* b) {
  A = a;
  B = b;
}

bool VertexPair::equals(VertexPair* rhs) {
  return (A->equals(rhs->A) && B->equals(rhs->B)) ||
    (A->equals(rhs->B) && B->equals(rhs->A));
}

// Note that I've reversed the negative signs for all of these rotations
// because we want to rotate clockwise, which means using a theta of -90deg

void Vertex::RotateX(int dir) {
  int y = Y;
  int z = Z;
  Y = -z * dir;
  Z = y * dir;
};

void Vertex::RotateY(int dir) {
  int x = X;
  int z = Z;
  X = -z * dir;
  Z = x * dir;
};

void Vertex::RotateZ(int dir) {
  int x = X;
  int y = Y;
  X = -y * dir;
  Y = x * dir;
};

void Vertex::Rotate(char axis, int dir, int x, int y, int z) {
  X = X - x;
  Y = Y - y;
  Z = Z - z;
  switch (axis) {
    case 'x':
      RotateX(dir);
      break;
    case 'y':
      RotateY(dir);
      break;
    case 'z':
      RotateZ(dir);
      break;
    default:
      break;
  }
  X = X + x;
  Y = Y + y;
  Z = Z + z;
}

string Cube::ToKey(int x, int y) {
  return to_string(x) + "," + to_string(y);
}

void CubeFace::AddTile(string key, Tile* t) {
  grid[key] = t;
}

CubeFace::CubeFace(int x, int y) {
  X = x;
  Y = y;

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
  Side2Vertices['>'] = new VertexPair(Vertices[0], Vertices[2]);
  Side2Vertices['<'] = new VertexPair(Vertices[1], Vertices[3]);
}

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
      int relativeX = x % FaceSize;
      int relativeY = y % FaceSize;
      next = new Tile(relativeX, relativeY, cur);
      string key = ToKey(relativeX, relativeY);
      face->AddTile(key, next);

      // Set the first tile
      if (first == NULL) {
        first = next;
      }
    }
  }

  return first;
}

Tile* Cube::GetNextSpace(char* facing, int x, int y) {
  // TODO
  return NULL;
}

bool CubeFace::HasNeighbor(CubeFace* neighbor) {
  try {
    char dir = Neighbor2Side.at(neighbor);
    return !!dir;
  } catch (out_of_range &oor) {
    return false;
  }
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

void RotateAllVertices(CubeFace* face, char axis, int dir, int x, int y, int z, map<CubeFace*, bool>* visited) {
  for (int i = 0; i < 4; i++) {
    face->Vertices[i]->Rotate(axis, dir, x, y, z);
  }
  visited->operator[](face) = true;
  for (int n = 0; n < face->AdjCnt; n++) {
    CubeFace* neigh = face->Neighbors[n];
    if (!visited->at(neigh)) {
      RotateAllVertices(neigh, axis, dir, x, y, z, visited);
    }
  }
  visited->operator[](face) = false;
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

// Rotate the 'b' face 90 degrees relative to the 'a' face.
// This means: find the axis that they have in common and rotate over it.
// I.e. we find the two vertices that the faces have in common, then
// find the axis that changes value between both of those vertices.
// E.g. (1,1,1) and (1,0,1) only differs on the y-axis, so we need
// to rotate all of the points around the y-axis
void RotateFace3D(CubeFace* a, CubeFace* b, map<CubeFace*, bool>* visited) {
  Vertex** shared = GetSharedVertices(a, b);
  // Now we find out what axis has different values and we rotate over that axis.
  Vertex* v1 = shared[0];
  Vertex* v2 = shared[1];
  int dir = 1; // Clockwise
  char facing = a->Neighbor2Side.at(b);
  if (facing == '>' || facing == 'v') {
    dir = 1;
  }
  if (v1->X != v2->X) {
    RotateAllVertices(b, 'x', 1, 0, v1->Y, v1->Z, visited);
  } else if (v1->Y != v2->Y) {
    RotateAllVertices(b, 'y', 1, v1->X, 0, v1->Z, visited);
  } else { // Rotate over z-axis
    RotateAllVertices(b, 'z', 1, v1->X, v1->Y, 0, visited);
  }

  delete[] shared; // Clean up, eh?
}

// Face-flipping logic:
// - Start with 1 -> flip it's neighbors, set flipped=true.
// -- All the neighbors of those neighbors should also flip, but don't mark
// - For each neighbor that was marked as flipped, flip it's neighbors and mark
// -- Recursively flip the neighbor's neighbors
// ...and so on
void Cube::FlipFaces() {
  // Populate the 'visited' collection
  CubeFace* cur;
  std::map<CubeFace*, bool> visited;
  for (int i = 0; i < FaceCnt; i++) {
    cur = Faces[i];
    visited[cur] = false;
  }
  // Mark the first as 'visited' so we don't flip it and enqueue it
  cur = Faces[0];
  queue<CubeFace*> Q;
  Q.push(cur);
  visited[cur] = true;

  // BFS!
  while (!Q.empty()) {
    cur = Q.front();
    Q.pop(); // Thanks, C++, for not returning the popped value
    CubeFace** neighbors = cur->Neighbors;
    for (int n = 0; n < cur->AdjCnt; n++) {
      CubeFace* neighbor = neighbors[n];
      // Process the neighbor if we haven't flipped it yet!
      if (!visited[neighbor]) {
        cout << "Rotating " << ToKey(neighbor->X, neighbor->Y) << " relative to " << ToKey(cur->X, cur->Y) << "\n";
        RotateFace3D(cur, neighbor, &visited);
        visited[neighbor] = true;
        Q.push(neighbor);
      }
    }
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
  
  PrintAllVertices();

  // Now that we have our cube, we need to go back through and find all the NEW edge
  // directions
}

void Cube::PrintAllVertices() {
  std::map<std::string, bool> unique;

  for (int f = 0; f < FaceCnt; f++) {
    CubeFace* face = Faces[f];
    Vertex** vertices = face->Vertices;
    for (int i = 0; i < 4; i++) {
      Vertex* v = vertices[i];
      string key = std::to_string(v->X) + std::to_string(v->Y) + std::to_string(v->Z);
      if (!unique[key]) {
        v->PrintVertex();
        unique[key] = true;
      }
    }
  }
}