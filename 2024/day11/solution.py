from template.Solution import Solution

# Recursive function with memoization, so if we hit a number
# we've seen with a particular number of blinks, we can short-circuit
def numStones(stone, blink, limit, memo):
  # Base cases
  key = f"{stone}-{blink}"
  print(key)
  if key in memo:
    return memo[key]
  if blink == limit:
    return 1

  val = 0
  if stone == "0":
    val += numStones("1", blink + 1, limit, memo)
  elif len(stone) % 2 == 0:
    mid = int(len(stone)/2)
    stone1 = str(int(stone[0:mid]))
    val += numStones(stone1, blink + 1, limit, memo)
    stone2 = str(int(stone[mid:]))
    val += numStones(stone2, blink + 1, limit, memo)
  else:
    val += numStones(str(int(stone)*2024), blink + 1, limit, memo)
  memo[key] = val
  return val

class Day11Solution(Solution):
  def __init__(self):
    super().__init__(11)
    self.part1 = True
    self.part2 = True

  # Just a BFS on the stones
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
  
  def Part2(self):
    stones = self.readInput()[0].split(" ")
    # The strategy is to do a DFS for each stone and keep updating the memo until we hit a depth of 75
    cnt = 0
    memo = {}
    while len(stones) > 0:
      stone = stones.pop()
      cnt += numStones(stone, 0, 75, memo)
    return cnt

  pass

urlpatterns = Day11Solution().urls()