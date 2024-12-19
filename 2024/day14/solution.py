from template.Solution import Solution
import math

# In case we want a video of all the PPM files...
# import io
# import os

class Robot:
  x = 0
  y = 0
  def __init__(self, input: str):
    [pos, vel] = input.split(" ")
    pos = pos[pos.index("=")+1:]
    [self.x, self.y] = list(map(int, pos.split(",")))
    vel = vel[vel.index("=")+1:]
    [self.dx, self.dy] = list(map(int, vel.split(",")))

  def move(self, width, height):
    self.x = (self.x + self.dx) % width
    self.y = (self.y + self.dy) % height

  # For debugging the parsing
  def __str__(self):
    return f"Robot at position ({self.x},{self.y}) with velocity {self.dx},{self.dy}"

class Day14Solution(Solution):
  def __init__(self):
    super().__init__(14)
    self.part1 = True
    self.part2 = True

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
  
  # This solution is quite slow because it does a BFS for every single
  # robot position on every single iteration. Not sure if there's a better
  # way to do this!
  def Part2(self):
    # if "tmp" not in os.listdir():
    #   os.mkdir("tmp")

    input = self.readInput()
    width = 101
    height = 103
    robots: list[Robot] = []
    for line in input:
      robots.append(Robot(line))

    # Populate the grid
    cnt  = 0
    grid: list[list[int]] = []
    for i in range(0, height):
      grid.append([])
      for j in range(0, width):
        grid[i].append(0)
    
    cnt = 0
    finalPosition = -1
    while cnt < width * height:
      # Reset the grid
      for i in range(0, height):
        for j in range(0, width):
          grid[i][j] = 0

      pos = []
      for robot in robots:
        x = ((robot.dx * cnt) + robot.x) % width
        y = ((robot.dy * cnt) + robot.y) % height
        grid[y][x] = 1
        pos.append([x, y])
      
      # BFS every robot...
      if finalPosition == -1:
        for [x, y] in pos:
          q = [[x, y]]
          visited = {}
          score = 0
          while len(q) > 0:
            [x, y] = q.pop(0)
            if f"{x},{y}" not in visited:
              visited[f"{x},{y}"] = True
              score += 1
              if y > 0 and grid[y - 1][x] == 1:
                q.append([x, y - 1])
              if y < height - 1 and grid[y + 1][x] == 1:
                q.append([x, y + 1])
              if x > 0 and grid[y][x - 1] == 1:
                q.append([x - 1, y])
              if x < width - 1 and grid[y][x + 1] == 1:
                q.append([x + 1, y])
            # Absolutely arbitrary score to try and find the secret image
            if score > 15:
              finalPosition = cnt
              break
          if finalPosition > -1:
            break
      # f = io.open(f"tmp/img-{cnt}.ppm", "w")
      # f.write("P1\n101 103\n")
      # f.write("\n".join(list(map(lambda x: "".join(x), grid))))
      # f.close()
      if finalPosition > -1:
        break
      cnt += 1
    # os.chdir("tmp")
    # os.system("ffmpeg -framerate 30 -i img-%d.ppm -c:v libx264 -crf 25 -vf 'scale=500:500,format=yuv420p' -movflags +faststart output.mp4")
    return finalPosition
  
  pass

urlpatterns = Day14Solution().urls()