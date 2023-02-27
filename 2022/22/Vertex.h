#ifndef VERTEX_H
#define VERTEX_H

#include <string>

class Vertex {
  public:
    int X;
    int Y;
    int Z;
    Vertex(int x, int y, int z);
    std::string ToString();
    void Rotate(char axis, int dir, int x, int y, int z);
    bool equals(Vertex* rhs);

  private:
    void RotateX(int dir);
    void RotateY(int dir);
    void RotateZ(int dir);
};

class VertexPair {
  public:
    Vertex* A;
    Vertex* B;
    VertexPair(Vertex* a, Vertex* b);
    bool equals(VertexPair* rhs);
};

#endif