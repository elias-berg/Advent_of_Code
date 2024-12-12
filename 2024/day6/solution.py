from template.Solution import Solution

turn = {"^": ">",
        ">": "v",
        "v": "<",
        "<": "^"}

nextSpace = {"^": lambda pos: [pos[0], pos[1] - 1],
             ">": lambda pos: [pos[0] + 1, pos[1]],
             "v": lambda pos: [pos[0], pos[1] + 1],
             "<": lambda pos: [pos[0] - 1, pos[1]]}

def posHash(pos):
  return str(pos[0]) + "," + str(pos[1])

class Day6Solution(Solution):
  def __init__(self):
    super().__init__(6)
    self.part1 = True

  def Part1(self):
    grid = self.readInput()
    rows = len(grid)
    cols = len(grid[0])
    position = [0, 0]
    direction = "^"
    # First, go through until we get the start position
    for y in range(0, rows):
      row = grid[y]
      x = row.find(direction)
      if x != -1:
        position = [x, y]
        break
    posDict = {}
    posDict[posHash(position)] = True
    posDict["count"] = 1
    # Now go through the loop~
    nextPos = nextSpace[direction](position)
    x = nextPos[0]
    y = nextPos[1]
    while (y >= 0 and y < rows) and (x >= 0 and x < cols):
      if grid[y][x] == "#":
        direction = turn[direction]
      else:
        if posHash(nextPos) not in posDict:
          posDict[posHash(nextPos)] = True
          posDict["count"] = posDict["count"] + 1
        position = nextPos
      # Onto the next position!
      nextPos = nextSpace[direction](position)
      x = nextPos[0]
      y = nextPos[1]
    return posDict["count"]

  pass

urlpatterns = Day6Solution().urls()