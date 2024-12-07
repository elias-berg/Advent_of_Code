from django.http import HttpResponse
from django.urls import include, path
from .part1 import solution as p1

def part1(request):
  print("Day 1 Part 1")
  print(request.body)
  return HttpResponse(p1())

urlpatterns = [
    # ex: /day1/part1
    path("part1", part1, name="part1")
]