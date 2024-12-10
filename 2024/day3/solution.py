from template.Solution import Solution
import re

class Day3Solution(Solution):
  def __init__(self):
    super().__init__(3)
    self.part1 = True
    self.part2 = True

  def evaluate(self, match, enabled=True):
    if enabled:
      num1 = int(match[4:match.index(",")])
      num2 = int(match[match.index(",")+1:-1])
      return num1 * num2
    else:
      return 0

  def Part1(self):
    lines = self.readInput()
    cnt = 0
    for line in lines:
      matches = re.findall("mul\([1-9]{1}\d{0,2},[1-9]{1}\d{0,2}\)", line)
      for match in matches:
        cnt = cnt + self.evaluate(match)
    return cnt

  def Part2(self):
    lines = self.readInput()
    cnt = 0

    # Those tricky bastards made it so instructions can wrap across lines,
    # though that didn't seem to be the case for Part 1...?
    allLines = ""
    for line in lines:
      allLines = allLines + line

    matches = re.findall("mul\([1-9]{1}\d{0,2},[1-9]{1}\d{0,2}\)|do\(\)|don't\(\)", allLines)
    enabled = True
    for match in matches:
      if match == "do()":
        enabled = True
      elif match == "don't()":
        enabled = False
      else:
        cnt = cnt + self.evaluate(match, enabled)
    return cnt
  
  # No need to implement anything else
  pass

urlpatterns = Day3Solution().urls()