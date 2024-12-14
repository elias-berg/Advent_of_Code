from template.Solution import Solution

class Day9Solution(Solution):
  def __init__(self):
    super().__init__(9)
    self.part1 = True

  def Part1(self):
    input = self.readInput()[0] # It's only one line!
    id = 0
    nodes = []
    isFree = False
    for num in input:
      cnt = int(num)
      for _ in range(0, cnt):
        nodes.append(id if not isFree else ".")
      if isFree:
        id = id + 1
      isFree = not isFree # Flip the flag each iteration
    # Now that we have all the nodes in place, time to do a two-pointer swap!
    front = 0
    back = len(nodes) - 1
    while front < back:
      while not nodes[front] == ".":
        front = front + 1
      while nodes[back] == ".":
        back = back - 1
      if front > back:
        break
      tmp = nodes[front]
      nodes[front] = nodes[back]
      nodes[back] = tmp
    # Now add them
    cnt = 0
    for i in range(0, nodes.index(".")):
      cnt = cnt + (i * nodes[i])
    return cnt

  pass

urlpatterns = Day9Solution().urls()