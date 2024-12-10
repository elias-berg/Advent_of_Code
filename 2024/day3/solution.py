from template.Solution import Solution
import re

class Day3Solution(Solution):
  def __init__(self):
    super().__init__(3)
    self.part1 = True

  def Part1(self):
    lines = self.readInput()
    cnt = 0
    for line in lines:
      matches = re.findall("mul\([1-9]{1}\d{0,2},[1-9]{1}\d{0,2}\)", line)
      for match in matches:
        num1 = int(match[4:match.index(",")])
        num2 = int(match[match.index(",")+1:-1])
        cnt = cnt + (num1 * num2)
    return cnt
  
  # No need to implement anything else
  pass

urlpatterns = Day3Solution().urls()