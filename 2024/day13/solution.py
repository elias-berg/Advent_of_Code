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
    self.part2 = True

  # This is pretty slow because it's absolutely exhaustive, despite memoization.
  # TODO: Figure out how to speed it up...
  def Part1(self):
    input = self.readInput()
    input.append("")
    # Read-loop
    tokens = 0
    while len(input) > 0:
      a = Button(input.pop(0), 3)
      b = Button(input.pop(0), 1)
      prize = Prize(input.pop(0))
      _ = input.pop(0) # Empty line

      minTokens = tryPresses(a, b, prize, 0, 0, 0, 0, 0, {})
      if minTokens < sys.maxsize:
        tokens += minTokens
    return tokens
  
  # Add 10000000000000 to the Prize X and Y...
  def Part2(self):
    input = self.readInput()
    input.append("")
    # Read-loop
    tokens = 0
    while len(input) > 0:
      a = Button(input.pop(0), 3)
      b = Button(input.pop(0), 1)
      p = Prize(input.pop(0))
      _ = input.pop(0) # Empty line
      p.x += 10_000_000_000_000
      p.y += 10_000_000_000_000

      # Here goes Eli's attempt at linear algebra, oh boy!
      # The approach was to use a1x + b1y = c1, then solve for x (note: a1 * x).
      # Then, use that and plug it in for x to then solve for y in a2x + b2y = c2.
      # So you end up with:
      # y = (a1*c2 - a2*c1) / (a1*b2 - a2*b1)
      #
      # Only if we get a whole number can we get a minimum number!
      denominator = (a.x * b.y) - (a.y * b.x)
      if not denominator == 0: # Dividing by 0 would be BAD
        numerator = (a.x * p.y) - (a.y * p.x)
        [bPresses, remainder] = divmod(numerator, denominator)
        if remainder == 0: # No partial presses!
          # We're making an assumption here that a.x is > 0 or else we'd hit a divide by 0 error
          # solving for x, since x = (c1 - b1y) / a1x
          numerator2 = (p.x - (b.x * bPresses))
          [aPresses, remainder] = divmod(numerator2, a.x)
          if remainder == 0: # No partial presses!
            print(f"A Presses: {aPresses}, B Presses: {bPresses}")
            tokens += (a.cost * aPresses) + (b.cost * bPresses)
    return tokens

  pass

urlpatterns = Day13Solution().urls()