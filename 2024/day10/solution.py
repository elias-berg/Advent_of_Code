from template.Solution import Solution

def dfs(grid, r, c, map):
  # Only add to the trail count if we haven't seen this top position yet
  if grid[r][c] == 9:
    pos = f"{r},{c}"
    if map is not None and pos in map:
      return 0
    else:
      if map is not None: map[pos] = True
      return 1
  # Evaluate each direction: up, down, left, and right
  val = 0
  if r + 1 < len(grid) and grid[r+1][c] == grid[r][c] + 1:
    val += dfs(grid, r+1, c, map)
  if r - 1 >= 0 and grid[r-1][c] == grid[r][c] + 1:
    val += dfs(grid, r-1, c, map)
  if c + 1 < len(grid[r]) and grid[r][c+1] == grid[r][c] + 1:
    val += dfs(grid, r, c+1, map)
  if c - 1 >= 0 and grid[r][c-1] == grid[r][c] + 1:
    val += dfs(grid, r, c-1, map)
  return val

class Day10Solution(Solution):
  def __init__(self):
    super().__init__(10)
    self.part1 = True
    self.part2 = True

  def Part1(self):
    grid = self.readInputAsGrid(asInt=True)
    # Find all trailheads and do a DFS from there
    cnt = 0
    for r in range(0, len(grid)):
      for c in range(0, len(grid[r])):
        if grid[r][c] == 0:
          # We hit a trailhead!
          cnt = cnt + dfs(grid, r, c, {})
    return cnt

  def Part2(self):
    grid = self.readInputAsGrid(asInt=True)
    # Find all trailheads and do a DFS from there
    cnt = 0
    for r in range(0, len(grid)):
      for c in range(0, len(grid[r])):
        if grid[r][c] == 0:
          # We hit a trailhead!
          cnt = cnt + dfs(grid, r, c, None)
    return cnt

  pass

urlpatterns = Day10Solution().urls()