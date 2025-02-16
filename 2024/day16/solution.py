from template.Solution import Solution
import sys

# Current Direction: [Clockwise, Counter-clockwise]
turn = {
  "^": [">", "<"],
  ">": ["v", "^"],
  "v": ["<", ">"],
  "<": ["^", "v"]
}

nextSpace = {
  "^": lambda pos: [pos[0], pos[1] - 1],
  ">": lambda pos: [pos[0] + 1, pos[1]],
  "v": lambda pos: [pos[0], pos[1] + 1],
  "<": lambda pos: [pos[0] - 1, pos[1]]
}

class Move:
  def __init__(self, x, y, dir, score, fromTurn = False):
    self.x = x
    self.y = y
    self.dir = dir
    self.score = score
    self.fromTurn = fromTurn

  def pos(self):
    return [self.x, self.y]

  def key(self):
    return f"{self.x},{self.y},{self.dir},{self.fromTurn}"

def solveBFS(grid, start, dir):
  first = Move(start[0], start[1], dir, 0)
  q = [first]
  memo = {}

  best = sys.maxsize

  while len(q) > 0:
    move = q.pop(0)

    if move.score > best:
      continue

    if grid[move.y][move.x] == "E":
      print("Hit the end!")
      best = move.score if move.score < best else best
      continue

    # Only try the move if it's unique and better
    if move.key() in memo and move.score > memo[move.key()]:
      continue
    memo[move.key()] = move.score

    [nX, nY] = nextSpace[move.dir](move.pos())
    if grid[nY][nX] != "#":
      q.append(Move(nX, nY, move.dir, move.score + 1))

    # Don't try to turn twice!
    if not move.fromTurn:
      for newDir in turn[move.dir]:
        [nX, nY] = nextSpace[newDir](move.pos())
        if grid[nY][nX] != "#":
          q.append(Move(move.x, move.y, newDir, move.score + 1000, True))

  return best


class Day16Solution(Solution):
  def __init__(self):
    super().__init__(16)
    self.part1 = True

  def Part1(self):
    grid = self.readInputAsGrid()
    # Starting position is always in the bottom-left
    start = [1, len(grid) - 2] # [x, y]
    dir = ">"
    
    # Start solving!
    return solveBFS(grid, start, dir)
  
urlpatterns = Day16Solution().urls()