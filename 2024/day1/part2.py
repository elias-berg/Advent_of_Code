
import os
import math
from django.conf import settings

dir = "day1/"

def readInput(fileName):
  input = open(os.path.join(settings.BASE_DIR, dir + fileName))
  return input.read().split("\n")

def solution(fileName="input.txt"):
  lines = readInput(fileName)
  lList = {}
  rList = []
  for line in lines:
    nums = line.split("   ")
    print(int(nums[0]))
    lList[int(nums[0])] = 0
    rList.append(int(nums[1]))
  for num in rList:
    if num in lList:
      lList[num] = lList[num] + 1

  cnt = 0
  for num in lList:
    cnt += (num * lList[num])

  return cnt