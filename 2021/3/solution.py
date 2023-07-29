#!/usr/bin/env python3

import sys
import time
import math

def now():
  return round(time.time() * 1000)

############
# Functions
# Helpers used by the "main" script.
############

# Reads the input file and parses it into a collection of coordinate-arrays
def readInput(fileName):
    input = open(fileName, "r")
    return input.read().split("\n")

def bitAryToDecimal(ary):
  val = 0
  for i in range(0, len(ary)):
    idx = -1 - i # Start from the back!
    bit = ary[idx]
    if bit == 1:
      val = val + round(math.pow(2, i))
  return val

#########
# Script
# Here be where the code runs
#########

# Some simple code to let a -sample modifier let us run the sample input
fileName = "input.txt"
if len(sys.argv) == 2 and sys.argv[1] == "-sample":
  fileName = "sample_input.txt"

lines = readInput(fileName)

start = now()
gamma = []
epsilon = []
# Loop over every bit in each line to get the most common
# and least common bits for gamma and epsilon values
for bit in range(0, len(lines[0])):
  cnt = [0, 0]
  for i in range(0, len(lines)):
    val = int(lines[i][bit])
    cnt[val] = cnt[val] + 1
  if cnt[0] > cnt[1]:
    gamma.append(0)
    epsilon.append(1)
  else: # No need to check for '='
    gamma.append(1)
    epsilon.append(0)
print("Part 1: " + str(bitAryToDecimal(gamma) * bitAryToDecimal(epsilon)) + " (" + str(now() - start) + "ms)\n")
