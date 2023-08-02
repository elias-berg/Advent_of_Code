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
    bit = int(ary[idx])
    if bit == 1:
      val = val + round(math.pow(2, i))
  return val

def part1(lines):
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
  return bitAryToDecimal(gamma) * bitAryToDecimal(epsilon)

def part2(lines):
  oxygen = []
  co2 = []
  # First loop to populate the initial arrays
  cnt = [0, 0]
  for i in range(0, len(lines)):
    val = int(lines[i][0]) # MSB
    cnt[val] = cnt[val] + 1
  # Filter the original lines down to what's appropriate for oxygen and co2
  if cnt[0] > cnt[1]:
    oxygen = list(filter(lambda line: line[0] == "0", lines))
    co2 = list(filter(lambda line: line[0] == "1", lines))
  elif cnt[1] >= cnt[0]:
    oxygen = list(filter(lambda line: line[0] == "1", lines))
    co2 = list(filter(lambda line: line[0] == "0", lines))

  size = len(lines[0])
  # First, do all the oxygen lines
  for bit in range(1, size):
    cnt = [0, 0]
    for i in range(0, len(oxygen)):
      val = int(oxygen[i][bit])
      cnt[val] = cnt[val] + 1
    if cnt[0] > cnt[1]:
      oxygen = list(filter(lambda numStr: numStr[bit] == "0", oxygen))
    elif cnt[1] >= cnt[0]:
      oxygen = list(filter(lambda numStr: numStr[bit] == "1", oxygen))
    if len(oxygen) == 1:
      break
  # Now do co2
  for bit in range(1, size):
    cnt = [0, 0]
    for i in range(0, len(co2)):
      val = int(co2[i][bit])
      cnt[val] = cnt[val] + 1
    if cnt[0] > cnt[1]:
      co2 = list(filter(lambda numStr: numStr[bit] == "1", co2))
    elif cnt[1] >= cnt[0]:
      co2 = list(filter(lambda numStr: numStr[bit] == "0", co2))
    if len(co2) == 1:
      break

  # Strings count as arrays!
  return bitAryToDecimal(oxygen[0]) * bitAryToDecimal(co2[0])

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
part1Val = part1(lines)
print("Part 1: " + str(part1Val) + " (" + str(now() - start) + "ms)")

start = now()
part2Val = part2(lines)
print("Part 1: " + str(part2Val) + " (" + str(now() - start) + "ms)")
