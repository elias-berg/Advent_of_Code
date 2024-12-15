from template.Solution import Solution

class Chunk:
  idx = -1
  size = 0
  value = None

  def __init__(self, idx, value):
    self.idx = idx
    self.size = 1
    self.value = value

  def incSize(self):
    self.size += 1

  def __str__(self) -> str:
    return f"Value: {self.value}, Idx: {self.idx}, Size: {self.size}"

def constructFileSystem(input) -> list:
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
  return nodes

class Day9Solution(Solution):
  def __init__(self):
    super().__init__(9)
    self.part1 = True
    self.part2 = True

  def Part1(self):
    input = self.readInput()[0] # It's only one line!
    nodes = constructFileSystem(input)
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

  def Part2(self):
    input = self.readInput(False)[0]
    nodes = constructFileSystem(input)
    # Find all of the free and file chunks of space, we'll use them to quickly iterate
    fileIdx = -1
    freeIdx = -1
    fileChunks = []
    freeChunks = []
    for i in range(0, len(nodes)):
      node = nodes[i]
      # Free Chunks
      if node == ".":
        if freeIdx > -1:
          freeChunks[-1].incSize()
        else: # First of the sequence
          freeIdx = i
          freeChunks.append(Chunk(freeIdx, "."))
      else:
        freeIdx = -1
      # File Chunks
      if not node == ".":
        if len(fileChunks) > 0 and not fileChunks[-1].value == node:
          fileIdx = -1
        if fileIdx > -1:
          fileChunks[-1].incSize()
        else: # First of the sequence
          fileIdx = i
          fileChunks.append(Chunk(fileIdx, node))
      else:
        fileIdx = -1

    # Okay, now we'll start filling in free chunks from the start with file chunks from the back
    while len(fileChunks) > 0:
      fileChunk = fileChunks.pop() # From the back is default
      for i in range(0, len(freeChunks)):
        freeChunk = freeChunks[i]
        if freeChunk.idx > fileChunk.idx:
          break
        if freeChunk.size >= fileChunk.size:
          # As soon as we find a free chunk to accomodate the file chunk, we stuff it in
          # Clear file and make free space
          nodes[fileChunk.idx:(fileChunk.idx + fileChunk.size)] = ["."] * fileChunk.size
          # Replace free space with file
          nodes[freeChunk.idx:(freeChunk.idx + fileChunk.size)] = [fileChunk.value] * fileChunk.size
          # Then, if the free chunk is empty, we remove it from the free spaces altogether
          freeChunk.idx += fileChunk.size
          freeChunk.size -= fileChunk.size
          if freeChunk.size == 0:
            freeChunks.pop(i)
          break

    # Now add them
    cnt = 0
    for i in range(0, len(nodes)):
      if not nodes[i] == ".":
        cnt = cnt + (i * nodes[i])
    return cnt

  pass

urlpatterns = Day9Solution().urls()