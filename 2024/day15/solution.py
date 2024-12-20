from template.Solution import Solution

nextSpace = {"^": lambda pos: [pos[0], pos[1] - 1],
             ">": lambda pos: [pos[0] + 1, pos[1]],
             "v": lambda pos: [pos[0], pos[1] + 1],
             "<": lambda pos: [pos[0] - 1, pos[1]]}

def tryMove(grid, curPos, nextPos, nextFunc) -> bool:
  [x, y] = curPos
  [nX, nY] = nextPos
  if grid[nY][nX] == "#":
    return False
  if grid[nY][nX] == ".":
    grid[nY][nX] = grid[y][x]
    return True
  if grid[nY][nX] == "O":
    couldMove = tryMove(grid, nextPos, nextFunc(nextPos), nextFunc)
    if couldMove:
      grid[nY][nX] = grid[y][x]
      return True
  return False

class Day15Solution(Solution):
  def __init__(self):
    super().__init__(15)
    self.part1 = True

  def Part1(self):
    input = self.readInput()

    grid = []
    directions = ""
    curPos = [0, 0]
    doneParsingGrid = False
    for [y, line] in enumerate(input):
      if line == "":
        doneParsingGrid = True
        continue
      if not doneParsingGrid:
        grid.append(list(map(str, line)))
        x = line.find("@")
        if not x == -1:
          curPos = [x, y]
      else:
        directions += line
    
    # Debug
    # print("\n".join(list(map(lambda x: "".join(x), grid))))
    # print(f"Starting position is at {startPos[0]},{startPos[1]}")

    for i in range(0, len(directions)):
      curDir = directions[i]
      # Try to move our robot
      nextFunc = nextSpace[curDir]
      nextPos = nextFunc(curPos)
      didMove = tryMove(grid, curPos, nextPos, nextFunc)
      if didMove:
        [x, y] = curPos
        grid[y][x] = "."
        curPos = nextPos
    
    #print("\n".join(list(map(lambda x: "".join(x), grid))))

    # We could keep a dict of all these, but the grid isn't big enough for this
    # to be thaaaat much of a performance problem
    cnt = 0
    for y in range(1, len(grid) - 1):
      for x in range(1, len(grid[y]) - 1):
        if grid[y][x] == "O":
          cnt += (100 * y) + x
    return cnt

  pass

urlpatterns = Day15Solution().urls()