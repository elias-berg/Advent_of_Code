from django.http import HttpResponse
from django.urls import path
from .part1 import solution as p1
from .part2 import solution as p2

def part1(request):
  print("Day 1 Part 1")
  print(request.body)
  return HttpResponse(p1())

def part2(request):
  print("Day 1 Part 2")
  print(request.body)
  return HttpResponse(p2())

urlpatterns = [
    # ex: /day1/part1
    path("part1", part1, name="part1"),
    # ex: /day1/part2
    path("part2", part2, name="part2")
]