from template.Solution import Solution

class Point:
  x = 0
  y = 0

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return f"{self.x},{self.y}"

class Bounds:
  minX = 0
  minY = 0
  maxX = 0
  maxY = 0

  def __init__(self, minX, minY, maxX, maxY):
    self.minX = minX
    self.minY = minY
    self.maxX = maxX
    self.maxY = maxY
  
  def hasPoint(self, p: Point) -> bool:
    return p.x >= self.minX and p.x <= self.maxX and p.y >= self.minY and p.y <= self.maxY

class Day8Solution(Solution):
  def __init__(self):
    super().__init__(8)
    self.part1 = True
    self.part2 = True

  def Part1(self):
    grid = self.readInputAsGrid()
		# Do a once-over just tracking the positions of every unique key
    nodeDict = {}
    maxY = len(grid)
    maxX = len(grid[0])
    bounds = Bounds(0, 0, maxX-1, maxY-1)
    for y in range(0, maxY):
      for x in range(0, maxX):
        val = grid[y][x]
        if val != ".":
          if val not in nodeDict:
            nodeDict[val] = []
          nodeDict[val].append(Point(x, y))
    # For the second pass, we want to place all of the antinodes
    antinodeDict = {}
    for key in nodeDict:
      nodes = nodeDict[key]
      # Find the diff between node[0] and node[1], node[0] and node[2]...
      while len(nodes) > 0:
        curNode = nodes.pop(0)
        for otherNode in nodes:
          # Diff!
          xDiff = curNode.x - otherNode.x
          yDiff = curNode.y - otherNode.y
          p1 = Point(curNode.x + xDiff, curNode.y + yDiff)
          p2 = Point(otherNode.x - xDiff, otherNode.y - yDiff)
          #print(str(curNode) + " -> " + str(otherNode) + " = " + str(p1) + " and " + str(p2))
          if bounds.hasPoint(p1): antinodeDict[str(p1)] = True
          if bounds.hasPoint(p2): antinodeDict[str(p2)] = True
    return len(antinodeDict)
  
  # This is nearly the same as Part 1, except we don't just create one point for each pair,
  # we keep trying to create points until they hit outside the bounds of the grid
  def Part2(self):
    grid = self.readInputAsGrid()
    nodeDict = {}
    maxY = len(grid)
    maxX = len(grid[0])
    bounds = Bounds(0, 0, maxX-1, maxY-1)
    for y in range(0, maxY):
      for x in range(0, maxX):
        val = grid[y][x]
        if val != ".":
          if val not in nodeDict:
            nodeDict[val] = []
          nodeDict[val].append(Point(x, y))
    antinodeDict = {}
    for key in nodeDict:
      nodes = nodeDict[key]
      nodeCount = len(nodes)
      while len(nodes) > 0:
        curNode = nodes.pop(0)
        for otherNode in nodes:
          xDiff = curNode.x - otherNode.x
          yDiff = curNode.y - otherNode.y
          # Here is where the difference lies...
          # Keep trying to add points in each direction until you go off-grid
          # But also, count the nodes themselves since there's at least two or else
          # we wouldn't get this far
          antinodeDict[str(curNode)] = True
          p1 = Point(curNode.x + xDiff, curNode.y + yDiff)
          while bounds.hasPoint(p1):
            antinodeDict[str(p1)] = True
            p1 = Point(p1.x + xDiff, p1.y + yDiff)
          
          antinodeDict[str(otherNode)] = True
          p2 = Point(otherNode.x - xDiff, otherNode.y - yDiff)
          while bounds.hasPoint(p2):
            antinodeDict[str(p2)] = True
            p2 = Point(p2.x - xDiff, p2.y - yDiff)
    return len(antinodeDict)

  pass

urlpatterns = Day8Solution().urls()