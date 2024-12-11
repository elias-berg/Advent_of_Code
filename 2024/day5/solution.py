from template.Solution import Solution
import math

class Day5Solution(Solution):
  def __init__(self):
    super().__init__(5)
    self.part1 = True

  def Part1(self):
    input = self.readInput()
    cnt = 0
    # First construct the dictionaries, but keep track of the empty line
    idx = 0
    pageDict = {}
    numLines = len(input)
    for i in range(0, numLines):
      idx = i
      if len(input[i]) == 0:
        break
      [p1, p2] = input[i].split("|")
      if p1 not in pageDict:
        pageDict[p1] = {}
      pageDict[p1][p2] = True
    # Then go backwards through the dependency chain so we only have to check the previous number
    for i in range(idx + 1, numLines):
      curLine = input[i].split(",")
      curLine.reverse()
      valid = True
      curSize = len(curLine)
      for j in range(1, curSize):
        prev = curLine[j-1]
        cur = curLine[j]
        if prev in pageDict and cur in pageDict[prev]:
          valid = False
          break
      if valid:
        mid = math.floor(curSize/2)
        print(mid)
        cnt = cnt + int(curLine[mid])

    return cnt

  pass

urlpatterns = Day5Solution().urls()