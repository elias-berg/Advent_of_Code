from template.Solution import Solution

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

class Day4Solution(Solution):
  def __init__(self):
    super().__init__(4)
    self.part1 = True

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
  
  pass

urlpatterns = Day4Solution().urls()