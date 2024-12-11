from template.Solution import Solution

# Recursive check for Part 1 to see if XMAS is spelled in a particular
# direction dictated by the `func`
def check(grid, y, x, iter, func):
  [newX, newY] = func(x, y)
  if newX < 0 or newX == len(grid[0]) or newY < 0 or newY == len(grid):
    return 0
  cur = grid[newY][newX]
  if iter == 0 and cur == "M":
    return check(grid, newY, newX, iter + 1, func)
  if iter == 1 and cur == "A":
    return check(grid, newY, newX, iter + 1, func)
  if iter == 2 and cur == "S":
    return 1
  return 0

# Check for Part 2 to see if an "A" is diagonally crossed by M and S in one direction.
# It takes two checks to thus confirm, using the alternate diagonal for the second check.
def check2(grid, y, x, func):
  [newX1, newY1, newX2, newY2] = func(x, y)
  # Bounds-check
  if newX1 < 0 or newX1 == len(grid[0]) or newY1 < 0 or newY1 == len(grid) or \
     newX2 < 0 or newX2 == len(grid[0]) or newY2 < 0 or newY2 == len(grid):
    return False
  return (grid[newY1][newX1] == "S" and grid[newY2][newX2] == "M") or \
    (grid[newY1][newX1] == "M" and grid[newY2][newX2] == "S")

class Day4Solution(Solution):
  def __init__(self):
    super().__init__(4)
    self.part1 = True
    self.part2 = True

  def Part1(self):
    grid = self.readInput()
    cnt = 0
    for y in range(0, len(grid)):
      for x in range(0, len(grid[y])):
        if grid[y][x] == "X":
          cnt = cnt + check(grid, y, x, 0, lambda x, y: [x, y - 1]) # Up
          cnt = cnt + check(grid, y, x, 0, lambda x, y: [x, y + 1]) # Down
          cnt = cnt + check(grid, y, x, 0, lambda x, y: [x - 1, y]) # Left
          cnt = cnt + check(grid, y, x, 0, lambda x, y: [x - 1, y - 1]) # Diag Up Left
          cnt = cnt + check(grid, y, x, 0, lambda x, y: [x - 1, y + 1]) # Diag Down Left
          cnt = cnt + check(grid, y, x, 0, lambda x, y: [x + 1, y]) # Right
          cnt = cnt + check(grid, y, x, 0, lambda x, y: [x + 1, y - 1]) # Diag Up Right
          cnt = cnt + check(grid, y, x, 0, lambda x, y: [x + 1, y + 1]) # Diag Down Right
    return cnt

  def Part2(self):
    grid = self.readInput()
    cnt = 0
    # Same strategy as part 1, except key off of the letter 'A' instead
    # and then check the diagonals
    for y in range(0, len(grid)):
      for x in range(0, len(grid[y])):
        if grid[y][x] == "A" and \
          check2(grid, y, x, lambda x, y: [x + 1, y + 1, x - 1, y - 1]) and \
          check2(grid, y, x, lambda x, y: [x - 1, y + 1, x + 1, y - 1]):
          cnt = cnt + 1

    return cnt
  
  pass

urlpatterns = Day4Solution().urls()