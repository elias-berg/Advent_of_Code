from template.Solution import Solution

def evalPart1(result, nums) -> bool:
	return evalPart1Helper(result, nums, 1, nums[0])
	
# Recursive helper
def evalPart1Helper(result, nums, idx, sum) -> bool:
	if idx == len(nums):
		return sum == result
	return evalPart1Helper(result, nums, idx + 1, sum + nums[idx]) or \
    evalPart1Helper(result, nums, idx + 1, sum * nums[idx])

class Day7Solution(Solution):
	def __init__(self):
		super().__init__(7)
		self.part1 = True

	def Part1(self):
		input = self.readInput()
		cnt = 0
		for line in input:
			# Convert
			[result, nums] = line.split(": ")
			result = int(result)
			nums = list(map(int, nums.split(" ")))
			# Evaluate each line where Part 1 only allows for + and *
			if evalPart1(result, nums):
				cnt = cnt + result
		return cnt

	pass

urlpatterns = Day7Solution().urls()