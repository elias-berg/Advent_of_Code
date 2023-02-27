#include <string>

#include "Vertex.h"

using namespace std;

Vertex::Vertex(int x, int y, int z) {
  X = x;
  Y = y;
  Z = z;
}

string Vertex::ToString() {
  return "(" + to_string(X) + "," + to_string(Y) + "," + to_string(Z) + ")";
}

bool Vertex::equals(Vertex* rhs)  {
  return X == rhs->X && Y == rhs->Y && Z == rhs->Z;
}

void Vertex::RotateX(int dir) {
  int y = Y;
  int z = Z;
  Y = z * dir;
  Z = -y * dir;
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
  X = y * dir;
  Y = -x * dir;
};

void Vertex::Rotate(char axis, int dir, int x, int y, int z) {
  X = X - x;
  Y = Y - y;
  Z = Z - z;
  if (axis == 'x') {
    RotateX(dir);
  } else if (axis == 'y') {
    RotateY(dir);
  } else { // Assuming 'z' here
    RotateZ(dir);
  }
  X = X + x;
  Y = Y + y;
  Z = Z + z;
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