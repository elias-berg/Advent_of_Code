from template.Solution import Solution

class Day12Solution(Solution):
  def __init__(self):
    super().__init__(12)
    self.part1 = True

  # The plan is to kick off a BFS
  def Part1(self):
    grid = self.readInputAsGrid()
    cnt = 0
    for r in range(0, len(grid)):
      for c in range(0, len(grid[r])):
        key = grid[r][c]
        if not key == " ": # We'll replace all of the farm spots with spaces to show we processed them
          # We're into a new region!
          area = 0
          perimeter = 0
          q = [[r, c]]
          # Start with marking the start space as seen
          seen = {
            f"{r},{c}": [r, c]
          }
          while len(q) > 0:
            [curR, curC] = q.pop()
            area += 1
            perimeter += 4
            # Above
            next = curR - 1
            if next >= 0 and grid[next][curC] == key:
              if f"{next},{curC}" not in seen: q.append([next, curC])
              seen[f"{next},{curC}"] = [next, curC]
              perimeter -= 1
            # Below
            next = curR + 1
            if next < len(grid) and grid[next][curC] == key:
              if f"{next},{curC}" not in seen: q.append([next, curC])
              seen[f"{next},{curC}"] = [next, curC]
              perimeter -= 1
            # Left
            next = curC - 1
            if next >= 0 and grid[curR][next] == key:
              if f"{curR},{next}" not in seen: q.append([curR, next])
              seen[f"{curR},{next}"] = [curR, next]
              perimeter -= 1
            # Right
            next = curC + 1
            if next < len(grid[curR]) and grid[curR][next] == key:
              if f"{curR},{next}" not in seen: q.append([curR, next])
              seen[f"{curR},{next}"] = [curR, next]
              perimeter -= 1
          # Clear the spaces once we've got the info for the region!
          for pos in seen:
            [curR, curC] = seen[pos]
            grid[curR][curC] = " "
          print(f"Region {key} ended with area: {area}, perimeter: {perimeter}")
          cnt += (area * perimeter)
    return cnt

  pass

urlpatterns = Day12Solution().urls()