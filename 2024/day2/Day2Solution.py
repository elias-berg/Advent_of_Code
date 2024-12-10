from template.Solution import Solution

class Day2Solution(Solution):
  def __init__(self):
    super().__init__(2)

  def part1(self):
    lines = self.readInput()

    cnt = 0
    for line in lines:
      nums = list(map(int, line.split(" ")))
      diff = 0
      safe = True # Whether or not we hit the end of the sequence; assume True, set to False ASAP
      for i in range(0, len(nums) - 1):
        newDiff = nums[i] - nums[i+1]
        if abs(newDiff) < 1 or abs(newDiff) > 3 or (newDiff < 0 and diff > 0) or (newDiff > 0 and diff < 0):
          safe = False
          break
        diff = newDiff
      if safe:
        cnt = cnt + 1
    return cnt
  
  pass