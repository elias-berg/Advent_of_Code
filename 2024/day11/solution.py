from template.Solution import Solution

class Day11Solution(Solution):
  def __init__(self):
    super().__init__(11)
    self.part1 = True

  # Just a BFS on the stones
  # TODO: Add memoization for speed?
  def Part1(self):
    input = self.readInput()[0].split(" ")
    stones = list(map(lambda x: [x, 0], input))
    cnt = 0
    while len(stones) > 0:
      [stone, blink] = stones.pop()
      if blink == 25:
        cnt += 1
      else:
        if stone == "0":
          stones.append(["1", blink + 1])
        elif len(stone) % 2 == 0:
          mid = int(len(stone)/2)
          stones.append([str(int(stone[0:mid])), blink + 1])
          stones.append([str(int(stone[mid:])), blink + 1])
        else:
          stones.append([str(int(stone)*2024), blink + 1])
    return cnt

  pass

urlpatterns = Day11Solution().urls()