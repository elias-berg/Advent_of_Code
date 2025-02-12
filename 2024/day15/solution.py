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

# Iterative BFS
def tryMove2(grid, curPos, nextFunc) -> bool:
  q = [curPos]
  visited = {}
  toMove = [] # Keep track of nodes to move if we can move at all
  while len(q) > 0:
    [x, y] = q.pop(0)
    
    key = f"{x},{y}"
    if key in visited:
      continue
    visited[f"{x},{y}"] = True

    [nx, ny] = nextFunc([x, y])
    toMove.append([x, y]) # Always track
    
    if grid[ny][nx] == "#":
      return False

    if grid[y][x] == "[":
      q.insert(0, [x+1, y])
    if grid[y][x] == "]":
      q.insert(0, [x-1, y])

    if grid[ny][nx] != ".":
      q.append([nx, ny])

  # If we got this far, then we can successfully move the load!
  while len(toMove) > 0:
    [x, y] = toMove.pop(0)
    # Cycle through to the leaf nodes
    [nx, ny] = nextFunc([x, y])
    if grid[ny][nx] == ".":
      grid[ny][nx] = grid[y][x]
      grid[y][x] = "."
    else:
      toMove.append([x, y])
    
  return True
  
class Day15Solution(Solution):
  def __init__(self):
    super().__init__(15)
    self.part1 = True
    self.part2 = True

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
  
  def Part2(self):
    input = self.readInput()

    # Setup and finding start
    grid = []
    directions = ""
    curPos = [0, 0]
    doneParsingGrid = False
    for [y, line] in enumerate(input):
      if line == "":
        doneParsingGrid = True
        continue
      if not doneParsingGrid:
        wideLine = []
        '''
        If the tile is #, the new map contains ## instead.
        If the tile is O, the new map contains [] instead.
        If the tile is ., the new map contains .. instead.
        If the tile is @, the new map contains @. instead.
        '''
        hasStart = False
        for c in list(map(str, line)):
          if c == "#":
            wideLine.append("#")
            wideLine.append("#")
          elif c == "O":
            wideLine.append("[")
            wideLine.append("]")
          elif c == ".":
            wideLine.append(".")
            wideLine.append(".")
          else:
            hasStart = True
            wideLine.append("@")
            wideLine.append(".")

        grid.append(wideLine)
        x = wideLine.index("@") if hasStart else -1
        if not x == -1:
          curPos = [x, y]
      else:
        directions += line

    #print("\n".join(list(map(lambda x: "".join(x), grid))))

    for i in range(0, len(directions)):
      curDir = directions[i]
      # Try to move our robot
      nextFunc = nextSpace[curDir]
      nextPos = nextFunc(curPos)
      didMove = tryMove2(grid, curPos, nextFunc)
      if didMove:
        curPos = nextPos
    
    #print("\n".join(list(map(lambda x: "".join(x), grid))))

    # We could keep a dict of all these, but the grid isn't big enough for this
    # to be thaaaat much of a performance problem
    cnt = 0
    for y in range(1, len(grid) - 1):
      for x in range(1, len(grid[y]) - 1):
        if grid[y][x] == "[":
          cnt += (100 * y) + x
    return cnt

  pass

urlpatterns = Day15Solution().urls()