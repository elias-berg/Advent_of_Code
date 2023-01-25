#!/usr/bin/env python3

# Advent of Code 2022 - Day 18
# Boiling Boulders
#
# You get out of the cave with the elephants, but lava is flowing out
# of the volcano past you into a pond. You scan a droplet flying by since
# the speed the lava will cool down is based on how big the droplets are.
# The device can only scan in low-resolution 1x1x1 coordinates, though.
#
# Part 1 -
# Given the input of all the 1x1x1 coodinates the lava "droplet" is
# comprised of, what is the surface area of the droplet?
#
# Part 2 -
# The cooling surface depends on all of the exterior-facing surfaces;
# any surface coordinate that's completely blocked on all 6 sides by
# surface area creates an air bubble that won't speed up the cooling.
# So what is the surface area of only the external surface area?

# To run:
# - python3 solution.py

# To run the sample input:
# - python3 solution.py -sample

import sys;

INPUT_FILE = "input.txt" # For ease-of-use

############
# Functions
# Helpers used by the "main" script.
############

# Reads the input file and parses it into a collection of coordinate-arrays
def readInput():
    input = open(INPUT_FILE, "r")
    coordLines = input.read().split("\n")
    coords = []
    for coordStr in coordLines:
      coords.append(str2coord(coordStr))
    return coords

# Converts a coordinate-string (e.g. "1,2,3") into an array format
# we we can evaluate it's neighbors easily, e.g. [1, 2, 3]
def str2coord(coordStr):
  coordAry = coordStr.split(",")
  return [int(coordAry[0]), int(coordAry[1]), int(coordAry[2])]

# Converts a coordinate-array (e.g. [1, 2, 3]) into a string format
# so we can use it as a dictionary key, e.g. "1,2,3"
def coord2str(coord):
  s = ""
  cLen = len(coord)
  for i in range(cLen):
    s = s + str(coord[i])
    if i < cLen - 1:
      s = s + ","
  return s

# Given the droplet dictionary, the copy of the coordinate string with an array position (x)
# and the new position value, edges the current coordinate's list of edges. If the edge already
# exists in the droplet, then we'll update both the edge-coordinate and current coordinate
# to not list each other
def updateEdges(droplet, edge, x, val, coordStr):
  edge[x] = edge[x] + val
  edgeStr = coord2str(edge)
  droplet[coordStr][edgeStr] = True # Make sure the dictionary entry exists first
  # Remove both entries if the edge already exists as a coordinate in the droplet
  if edgeStr in droplet:
    del droplet[coordStr][edgeStr]
    del droplet[edgeStr][coordStr]

# Given a coordinate-array (e.g. [1, 2, 3]), adds all of its possible edges to a dictionary
# mapped the droplet dictionary via the coordinate as a string
# E.g. droplet["1,2,3"] = {"2,2,3": True, "0,2,3": True, ..., "1,2,2": true}
def addSurface(droplet, coord):
  coordStr = coord2str(coord)
  droplet[coordStr] = {} # We're guaranteed the coord hasn't been seen yet

  for x in range(3):
    edge = coord.copy()
    updateEdges(droplet, edge, x, 1, coordStr)
    updateEdges(droplet, edge, x, -2, coordStr) # Need to -2 to offset the extra 1 we added

# Given a starting edge, breadth-first-search until
def removeOutsideEdges(droplet, edges, entireMap, minCoord):
  visited = {}
  firstCoord = coord2str([minCoord, minCoord, minCoord])
  Q = [firstCoord]
  
  while len(Q) > 0:
    curCoordStr = Q.pop()
    visited[curCoordStr] = True

    # If the coordinate we have come across is in the list of edges,
    # then it means it's an outside edge and we should remove it
    if curCoordStr in edges:
      del edges[curCoordStr]

    curCoord = str2coord(curCoordStr)
    for x in range(3):
      copyCoord = curCoord.copy()
      copyCoord[x] = curCoord[x] + 1
      copyCoordStr = coord2str(copyCoord)
      if copyCoordStr in entireMap and \
         copyCoordStr not in droplet and \
         copyCoordStr not in visited:
        Q.append(copyCoordStr)

      copyCoord[x] = curCoord[x] - 1
      copyCoordStr = coord2str(copyCoord)
      if copyCoordStr in entireMap and \
         copyCoordStr not in droplet and \
         copyCoordStr not in visited:
        Q.append(copyCoordStr)

#########
# Script
# Here be where the code runs
#########

# Some simple code to let a -sample modifier let us run the sample input
if len(sys.argv) == 2 and sys.argv[1] == "-sample":
  INPUT_FILE = "sample_input.txt"

coords = readInput()

# Construct the droplet
droplet = {} # It's a map of maps
# We also want to keep track of the min and max x/y/z coordinate values
minCoord = 100 # Should be safe to make it only this high
maxCoord = 0
for coord in coords:
  addSurface(droplet, coord)
  # Find the mix/max bounds of the entire 3D structure (for Part 2)
  for pos in coord:
    if pos > maxCoord:
      maxCoord = pos
    if pos < minCoord:
      minCoord = pos

# Now count all of the uncovered surfaces of each coordinate of the droplet
part1 = 0
edgeDict = {}
for coordStr in droplet.keys():
  part1 = part1 + len(droplet[coordStr]) # The length is the number of surface coordinates

  # While we're looping through, let's count up the number of coordinates that share
  # an "edge". This will be the value we subtract if we find the edge is contained
  # in a bubble (doesn't reach outside air for part 2).
  for edgeStr in droplet[coordStr]:
    if edgeStr not in edgeDict:
      edgeDict[edgeStr] = 1
    else:
      edgeDict[edgeStr] = edgeDict[edgeStr] + 1

print("Part 1: " + str(part1))

# For part 2, we'll create an entire mapping of the 3D coordinates with 1 extra unit in
# each direction to represent the "outside"
minCoord = minCoord - 1
maxCoord = maxCoord + 2 # Add an extra 1 since the "range" function is non-inclusive
entireMap = {}
for x in range(minCoord, maxCoord):
  for y in range(minCoord, maxCoord):
    for z in range(minCoord, maxCoord):
      entireMap[coord2str([x, y, z])] = True

# Now for part 2, we'll start from an outermost corner and BFS our way to the
# opposite corner, removing all edges we meet
removeOutsideEdges(droplet, edgeDict, entireMap, minCoord)

part2 = 0
for edgeStr in edgeDict.keys():
  part2 = part2 + edgeDict[edgeStr]

print("Part 2: " + str(part1 - part2))
