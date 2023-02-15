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

void CubeFace::AddTile(string key, Tile* t) {
  grid[key] = t;
}

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

string CubeFace::ToString() {
  return to_string(X) + "," + to_string(Y);
}

Tile* Cube::GetNextSpace(char* facing, int x, int y) {
  // TODO
  cout << "TO DO\n";
  return NULL;
}

bool CubeFace::HasNeighbor(CubeFace* neighbor) {
  try {
    char dir = Neighbor2Side.at(neighbor);
    return dir == '>' || dir == '<' || dir == 'v' || dir == '^';
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

  PrintAllNeighbors();
}

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