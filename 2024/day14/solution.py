from template.Solution import Solution
import math

class Robot:
  def __init__(self, input: str):
    [pos, vel] = input.split(" ")
    pos = pos[pos.index("=")+1:]
    [self.x, self.y] = list(map(int, pos.split(",")))
    vel = vel[vel.index("=")+1:]
    [self.dx, self.dy] = list(map(int, vel.split(",")))

  # For debugging the parsing
  def __str__(self):
    return f"Robot at position ({self.x},{self.y}) with velocity {self.dx},{self.dy}"


class Day14Solution(Solution):
  def __init__(self):
    super().__init__(14)
    self.part1 = True

  def Part1(self):
    useSample = False
    input = self.readInput(useSample)
    width = 101 if not useSample else 11 # 0...100
    height = 103 if not useSample else 7 # 0...102
    midH = math.floor(height / 2) if not useSample else 5
    midW = math.floor(width / 2) if not useSample else 3
    quads = [0, 0, 0, 0] # -> Top Left, Bottom Left, Top Right, Bottom Right
    for line in input:
      robot = Robot(line)
      x = ((robot.dx * 100) + robot.x) % width
      y = ((robot.dy * 100) + robot.y) % height
      #print(f"Robot ends up at {x},{y}") # Debug
      if x < midW and y < midH: quads[0] += 1
      if x < midW and y > midH: quads[1] += 1
      if x > midW and y < midH: quads[2] += 1
      if x > midW and y > midH: quads[3] += 1
    return quads[0] * quads[1] * quads[2] * quads[3]

  pass

urlpatterns = Day14Solution().urls()