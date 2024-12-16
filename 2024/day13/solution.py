from typing import Self
from template.Solution import Solution
import re
import sys

class XY:
  def __str__(self):
    return f"{type(self).__name__}: X+{self.x}, Y+{self.y}"

class Button(XY):
  def __init__(self, input, cost):
    matches = re.findall("X\+\d+|Y\+\d+", input)
    self.x = int(matches[0][2:])
    self.y = int(matches[1][2:])
    self.cost = cost

class Prize(XY):
  def __init__(self, input):
    matches = re.findall("X\=\d+|Y\=\d+", input)
    self.x = int(matches[0][2:])
    self.y = int(matches[1][2:])

def tryPresses(a: Button, b: Button, p: Prize, tokens: int, x: int, y: int, aPresses: int, bPresses: int, memo: dict):
  key = f"{aPresses},{bPresses},{x},{y}"
  if key in memo:
    return memo[key]
  if x > p.x:
    return sys.maxsize
  if y > p.y:
    return sys.maxsize
  if y == p.y and x == p.x:
    return tokens
  
  # Try B first, then try A
  minTokens = sys.maxsize
  if bPresses < 100:
    newMin = tryPresses(a, b, p, tokens + b.cost, x + b.x, y + b.y, aPresses, bPresses + 1, memo)
    if newMin < minTokens:
      minTokens = newMin
  if aPresses < 100:
    newMin = tryPresses(a, b, p, tokens + a.cost, x + a.x, y + a.y, aPresses + 1, bPresses, memo)
    if newMin < minTokens:
      minTokens = newMin
  memo[key] = minTokens
  return minTokens
  

class Day13Solution(Solution):
  def __init__(self):
    super().__init__(13)
    self.part1 = True

  # This is pretty slow because it's absolutely exhaustive, despite memoization.
  # TODO: Figure out how to speed it up...
  def Part1(self):
    input = self.readInput()
    # Read-loop
    tokens = 0
    while len(input) > 0:
      a = input.pop(0)
      if a == "": # In case of empty row
        a = input.pop(0)
      a = Button(a, 3)
      b = Button(input.pop(0), 1)
      prize = Prize(input.pop(0))

      minTokens = tryPresses(a, b, prize, 0, 0, 0, 0, 0, {})
      if minTokens < sys.maxsize:
        tokens += minTokens
    return tokens

  pass

urlpatterns = Day13Solution().urls()