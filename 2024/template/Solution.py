import os
from django.conf import settings
from django.http import HttpResponse
from django.urls import path

class Solution:
  def __init__(self, day):
    self.day = f"day{day}" # For reading the input files
    self.part1 = False
    self.part2 = False

  def Part1(self) -> int:
    return 0
  
  def Part2(self) -> int:
    return 0

  def readInput(self, fileName="input.txt") -> str:
    input = open(os.path.join(settings.BASE_DIR, self.day + "/" + fileName))
    return input.read().split("\n")
  
  def urls(self) -> list:
    parts = []
    if self.part1:
      parts.append(path("part1", lambda _: HttpResponse(self.Part1()), name="part1"))
    if self.part2:
      parts.append(path("part2", lambda _: HttpResponse(self.Part2()), name="part2"))
    return parts