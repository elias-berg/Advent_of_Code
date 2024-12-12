from template.Solution import Solution
import math

class Day5Solution(Solution):
  def __init__(self):
    super().__init__(5)
    # Do the parsing as a part of initialization since both parts need it
    self._makePageDict()
    self.part1 = True
    self.part2 = True

  # Populates self.dependencies with the page dependencies and self.sequences with
  # all the subsequent sequences we should be parsing out after the page dependencies
  def _makePageDict(self):
    input = self.readInput()
    self.dependencies = {}
    numLines = len(input)
    idx = 0
    for i in range(0, numLines):
      idx = i
      if len(input[i]) == 0:
        break
      [p1, p2] = input[i].split("|")
      if p1 not in self.dependencies:
        self.dependencies[p1] = {}
      self.dependencies[p1][p2] = True
    self.sequences = input[idx + 1: numLines]

  def _isValidSequence(self, nums):
    valid = True
    for i in range(1, len(nums)):
      prev = nums[i-1]
      cur = nums[i]
      # Because the `nums` array is reversed, the previous number (to the left of the current)
      # cannot have the current number as a dependency -> invalid!
      if prev in self.dependencies and cur in self.dependencies[prev]:
        valid = False
        break
    return valid

  def Part1(self):
    cnt = 0
    # Go backwards through the dependency chain so we only have to check the previous number
    for sequence in self.sequences:
      nums = sequence.split(",")
      nums.reverse()
      if self._isValidSequence(nums):
        mid = math.floor(len(nums)/2)
        cnt = cnt + int(nums[mid])
    return cnt

  def Part2(self):
    cnt = 0
    for sequence in self.sequences:
      nums = sequence.split(",")
      nums.reverse()
      size = len(nums)
      if not self._isValidSequence(nums):
        for i in range(1, size):
          prev = nums[i-1]
          cur = nums[i]
          if prev in self.dependencies and cur in self.dependencies[prev]:
            # Do a bubble sort on the sequence:
            # If the current number cannot come before the prev, swap...
            # Then re-evaluate until the current number moves all the way out of the way
            nums[i-1] = cur
            nums[i] = prev
            # Now iterate in reverse to bubble sort
            for j in range(i-1, 0, -1):
              newPrev = nums[j-1]
              if newPrev in self.dependencies and cur in self.dependencies[newPrev]:
                nums[j-1] = cur
                nums[j] = newPrev
        # nums.reverse() # This was for debugging
        mid = math.floor(size/2)
        cnt = cnt + int(nums[mid])
    return cnt

  pass

urlpatterns = Day5Solution().urls()