from template.Solution import Solution

turn = {"^": ">",
        ">": "v",
        "v": "<",
        "<": "^"}

nextSpace = {"^": lambda pos: [pos[0], pos[1] - 1],
             ">": lambda pos: [pos[0] + 1, pos[1]],
             "v": lambda pos: [pos[0], pos[1] + 1],
             "<": lambda pos: [pos[0] - 1, pos[1]]}

def posHash(pos) -> str:
  return str(pos[0]) + "," + str(pos[1])

def dehashPos(pos: str):
  return list(map(int, pos.split(",")))

def posDirHash(pos, dir) -> str:
  return posHash(pos) + dir

class Day6Solution(Solution):
  posDict = None

  def __init__(self):
    super().__init__(6)
    self.part1 = True
    self.part2 = True

  def _addPositionToDict(self, position):
    if self.posDict == None:
      self.posDict = {}
      self.posDict["count"] = 0
    if posHash(position) not in self.posDict:
      self.posDict[posHash(position)] = True
      self.posDict["count"] = self.posDict["count"] + 1
    

  def Part1(self) -> int:
    self.grid = self.readInput()
    self.rows = len(self.grid)
    self.cols = len(self.grid[0])
    curPos = [0, 0]
    direction = "^"
    # First, go through until we get the start position
    for y in range(0, self.rows):
      row = self.grid[y]
      x = row.find(direction)
      self.grid[y] = list(map(str, row)) # Convert to an array so we can assign temp values for Part 2
      if x != -1:
        curPos = [x, y]
    self.startPosition = curPos
    self._addPositionToDict(curPos)
    # Now go through the loop~
    curPos = self.startPosition
    nextPos = nextSpace[direction](curPos)
    x = nextPos[0]
    y = nextPos[1]
    while (y >= 0 and y < self.rows) and (x >= 0 and x < self.cols):
      if self.grid[y][x] == "#":
        direction = turn[direction]
      else:
        self._addPositionToDict(nextPos)
        curPos = nextPos
      # Onto the next position!
      nextPos = nextSpace[direction](curPos)
      x = nextPos[0]
      y = nextPos[1]
    return self.posDict["count"]

  # This is very slow because we go through EVERY space and try to see if it's a valid block to cause a loop
  # So it works as O(n^2) where n is the total number of rows * columns. Oof.
  # TODO: Find a way to speed this up?
  def Part2(self):
    # Re-complete Part 1 to get all of the viable positions
    self.Part1()
    # But remove the start position because we can't place a 
    self.posDict.pop(posHash(self.startPosition))
    self.posDict.pop("count")

    # Now, we'll go through each position and try to see if we hit a cycle for each;
    # If we hit a spot we've already been at before with the same direction, then we hit a cycle
    cnt = 0
    for positionHash in self.posDict:
      [sX, sY] = dehashPos(positionHash)
      self.grid[sY][sX] = "#"

      # Loop
      direction = "^"
      curPos = self.startPosition
      posDirDict = {}
      posDirDict[posDirHash(curPos, direction)] = True # Always mark the start

      nextPos = nextSpace[direction](curPos)
      x = nextPos[0]
      y = nextPos[1]
      while (y >= 0 and y < self.rows) and (x >= 0 and x < self.cols):
        if self.grid[y][x] == "#":
          direction = turn[direction]
        else:
          posDir = posDirHash(nextPos, direction)
          if posDir in posDirDict:
            cnt = cnt + 1
            break
          else:
            posDirDict[posDir] = True
          curPos = nextPos
        # Onto the next position!
        nextPos = nextSpace[direction](curPos)
        x = nextPos[0]
        y = nextPos[1]

      # Reset
      self.grid[sY][sX] = "."
    return cnt

  pass

urlpatterns = Day6Solution().urls()