from template.Solution import Solution

class Day12Solution(Solution):
  def __init__(self):
    super().__init__(12)
    self.part1 = True
    self.part2 = True

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
          cnt += (area * perimeter)
    return cnt
  
  # This is mostly the same as Part 1, except we need to keep track of the sides of the regions.
  # The strategy here is to add a "side" to a map of unique sides whenever a plot doesn't have
  # a neighbor of the same plot value.
  def Part2(self):
    grid = self.readInputAsGrid()
    cnt = 0
    for r in range(0, len(grid)):
      for c in range(0, len(grid[r])):
        key = grid[r][c]
        if not key == " ":
          area = 0
          sides = {} # Keep track of unique sides!
          q = [[r, c]]
          seen = {
            f"{r},{c}": [r, c]
          }
          while len(q) > 0:
            [curR, curC] = q.pop()
            area += 1

            # Above
            next = curR - 1
            if next >= 0 and grid[next][curC] == key:
              if f"{next},{curC}" not in seen:
                q.append([next, curC])
                seen[f"{next},{curC}"] = [next, curC]
            else: # If the neighboring plot is out of bounds or not the same value -> side!
              sideKey = f"^{curR}"
              if sideKey not in sides:
                sides[sideKey] = []
              sides[sideKey].append(curC)

            # Below
            next = curR + 1
            if next < len(grid) and grid[next][curC] == key:
              if f"{next},{curC}" not in seen:
                q.append([next, curC])
                seen[f"{next},{curC}"] = [next, curC]
            else:
              sideKey = f"v{curR}"
              if sideKey not in sides:
                sides[sideKey] = []
              sides[sideKey].append(curC)

            # Left
            next = curC - 1
            if next >= 0 and grid[curR][next] == key:
              if f"{curR},{next}" not in seen:
                q.append([curR, next])
                seen[f"{curR},{next}"] = [curR, next]
            else:
              sideKey = f"<{curC}"
              if sideKey not in sides:
                sides[sideKey] = []
              sides[sideKey].append(curR)

            # Right
            next = curC + 1
            if next < len(grid[curR]) and grid[curR][next] == key:
              if f"{curR},{next}" not in seen:
                q.append([curR, next])
                seen[f"{curR},{next}"] = [curR, next]
            else:
              sideKey = f">{curC}"
              if sideKey not in sides:
                sides[sideKey] = []
              sides[sideKey].append(curR)

          # Now we need to consolidate all of the sides...
          # Really the "sides" are just X,Y positions of other plots where:
          # - A ^{idx} or v{idx} is a plot at that Y idx creating a horizontal side with the array X positions
          # - A <{idx} or >{idx} is a plot at that X idx creating a vertical side with the array Y positions
          # e.g. sideArray["v3"] = [1, 2] would mean there are plots at (1,3) and (2,3), hence a horizontal side
          sideCnt = 0
          for sideKey in sides:
            sideAry = sides[sideKey]
            sideAry.sort()
            # We can start with the first index and increase the non-contiguous side count
            side = sideAry.pop(0)
            sideCnt += 1
            while len(sideAry) > 0:
              nextSide = sideAry.pop(0)
              # If we hit two numbers that are the same, it means it's a new side from a different position
              if not side + 1 == nextSide:
                sideCnt += 1
              side = nextSide

          # Clear the spaces once we've got the info for the region!
          for pos in seen:
            [curR, curC] = seen[pos]
            grid[curR][curC] = " "

          cnt += (area * sideCnt)
    return cnt

  pass

urlpatterns = Day12Solution().urls()