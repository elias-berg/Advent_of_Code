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

# To run:
# - python3 solution.py

# To run the sample input:
# - python3 solution.py -sample

import sys;

INPUT_FILE = "input.txt" # For ease-of-use

# Reads the input file and parses it into a collection of coordinate-arrays
def readInput():
    input = open(INPUT_FILE, "r")
    coordLines = input.read().split("\n")
    coords = []
    for coordStr in coordLines:
      coordAry = coordStr.split(",")
      coords.append([int(coordAry[0]), int(coordAry[1]), int(coordAry[2])])
    return coords

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

# "main"
# Here be where the code runs

# Some simple code to let a -sample modifier let us run the sample input
if len(sys.argv) == 2 and sys.argv[1] == "-sample":
  INPUT_FILE = "sample_input.txt"

coords = readInput()

# Construct the droplet
droplet = {} # It's a map of maps
for coord in coords:
  addSurface(droplet, coord)

# Now count all of the uncovered surfaces of each coordinate of the droplet
count = 0
for coord in droplet.keys():
  count = count + len(droplet[coord])
print("Part 1: " + str(count))