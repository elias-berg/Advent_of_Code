from template.Solution import Solution

class Day2Solution(Solution):
  def __init__(self):
    super().__init__(2)
    self.part1 = True
    self.part2 = True

  def isReportSafe(self, report):
    diff = 0
    for i in range(0, len(report) - 1):
      newDiff = report[i] - report[i+1]
      if abs(newDiff) < 1 or abs(newDiff) > 3 or (newDiff < 0 and diff > 0) or (newDiff > 0 and diff < 0):
        return False
      diff = newDiff
    return True

  def Part1(self):
    lines = self.readInput()

    cnt = 0
    for line in lines:
      nums = list(map(int, line.split(" ")))
      if self.isReportSafe(nums):
        cnt = cnt + 1
    return cnt
  
  def Part2(self):
    lines = self.readInput()

    cnt = 0
    for line in lines:
      nums = list(map(int, line.split(" ")))
      if self.isReportSafe(nums):
        cnt = cnt + 1
      # Basically just take part 1 and run it back for the list without individual values missing
      else:
        size = len(nums)
        for i in range(0, len(nums)):
          nums2 = nums[0:i] + nums[i+1:size]
          if self.isReportSafe(nums2):
            cnt = cnt + 1
            break
    return cnt
  
  # No need to implement anything else
  pass

urlpatterns = Day2Solution().urls()