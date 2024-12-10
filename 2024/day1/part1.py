
import os
from django.conf import settings

dir = "day1/"

def readInput(fileName):
  input = open(os.path.join(settings.BASE_DIR, dir + fileName))
  return input.read().split("\n")

def solution(fileName="input.txt"):
  lines = readInput(fileName)
  ary1 = []
  ary2 = []
  for line in lines:
    nums = line.split("   ")
    print(int(nums[0]))
    ary1.append(int(nums[0]))
    ary2.append(int(nums[1]))
  ary1.sort()
  ary2.sort()

  cnt = 0
  for i in range(0, len(ary1)):
    cnt += abs(ary1[i] - ary2[i])

  return cnt