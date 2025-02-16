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
  def __init__(self, x, y, dir, score, fromTurn = False, prevMove = None):
    self.x = x
    self.y = y
    self.dir = dir
    self.score = score
    self.fromTurn = fromTurn
    # The previous move that lead to this move, used for Part 2
    self.prevMove = prevMove

  def pos(self):
    return [self.x, self.y]

  def key(self):
    return f"{self.x},{self.y},{self.dir},{self.fromTurn}"
  
  # For indexing the specific position of the move, used for Part 2
  def posKey(self):
    return f"{self.x},{self.y}"

def solveBFS(grid, first: Move):
  q = [first]
  memo = {}

  best = sys.maxsize

  while len(q) > 0:
    move = q.pop(0)

    if move.score > best:
      continue

    if grid[move.y][move.x] == "E":
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

def solveBFS2(grid, first: Move, best):
  q = [first]
  memo = {}

  endMoves: list[Move] = []

  while len(q) > 0:
    move = q.pop(0)

    if move.score > best:
      continue

    if grid[move.y][move.x] == "E":
      endMoves.append(move)
      continue

    # Only try the move if it's unique and better
    if move.key() in memo and move.score > memo[move.key()]:
      continue
    memo[move.key()] = move.score

    [nX, nY] = nextSpace[move.dir](move.pos())
    if grid[nY][nX] != "#":
      q.append(Move(nX, nY, move.dir, move.score + 1, False, move))

    # Don't try to turn twice!
    if not move.fromTurn:
      for newDir in turn[move.dir]:
        [nX, nY] = nextSpace[newDir](move.pos())
        if grid[nY][nX] != "#":
          q.append(Move(move.x, move.y, newDir, move.score + 1000, True, move))

  # Now that we have all the moves that got us to the end, plus their chains,
  # we can iterate through and log all the unique seats in the maze
  seatMap = {}
  while len(endMoves) > 0:
    move = endMoves.pop()
    seatMap[move.posKey()] = True
    prevMove: Move = move.prevMove
    while prevMove is not None:
      seatMap[prevMove.posKey()] = True
      prevMove = prevMove.prevMove

  return len(seatMap)

class Day16Solution(Solution):
  def __init__(self):
    super().__init__(16)
    self.part1 = True
    self.part2 = True

  def Part1(self):
    grid = self.readInputAsGrid()
    # Starting position is always in the bottom-left
    start = [1, len(grid) - 2] # [x, y]
    
    # Start solving!
    return solveBFS(grid, Move(start[0], start[1], ">", 0))
  
  def Part2(self):
    grid = self.readInputAsGrid()
    # Starting position is always in the bottom-left
    start = [1, len(grid) - 2] # [x, y]
    
    # Once we have the best path, we actually want to then find all
    # the routes that get that best path...
    first = Move(start[0], start[1], ">", 0)
    best = solveBFS(grid, first)
    return solveBFS2(grid, first, best)
  
urlpatterns = Day16Solution().urls()