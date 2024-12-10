import os
from django.conf import settings
from django.http import HttpResponse
from django.urls import path

class Solution:
  def __init__(self, day):
    self.day = f"day{day}"
    self.part1Done = False
    self.part2Done = False

  def part1(self):
    return 0
  
  def part2(self):
    return 0

  def readInput(self, fileName="input.txt"):
    input = open(os.path.join(settings.BASE_DIR, self.day + "/" + fileName))
    return input.read().split("\n")
  
  def urls(self):
    parts = []
    if self.part1Done:
      parts.append(path("part1", lambda _: HttpResponse(self.part1()), name="part1"))
    if self.part2Done:
      parts.append(path("part2", lambda _: HttpResponse(self.part2()), name="part2"))
    return parts