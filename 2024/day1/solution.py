from template.Solution import Solution

class Day1Solution(Solution):
  def __init__(self):
    super().__init__(1)
    self.part1 = True
    self.part2 = True

  def Part1(self):
    lines = self.readInput()
    ary1 = []
    ary2 = []
    for line in lines:
      nums = line.split("   ")
      ary1.append(int(nums[0]))
      ary2.append(int(nums[1]))
    ary1.sort()
    ary2.sort()

    cnt = 0
    for i in range(0, len(ary1)):
      cnt += abs(ary1[i] - ary2[i])
    return cnt
  
  def Part2(self):
    lines = self.readInput()
    lList = {}
    rList = []
    for line in lines:
      nums = line.split("   ")
      lList[int(nums[0])] = 0
      rList.append(int(nums[1]))
    for num in rList:
      if num in lList:
        lList[num] = lList[num] + 1

    cnt = 0
    for num in lList:
      cnt += (num * lList[num])
    return cnt

  # No need to implement anything else
  pass

urlpatterns = Day1Solution().urls()