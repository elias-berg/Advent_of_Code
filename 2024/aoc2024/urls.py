"""
URL configuration for aoc2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("day1/", include("day1.solution")),
    path("day2/", include("day2.solution")),
    path("day3/", include("day3.solution")),
    path("day4/", include("day4.solution")),
    path("day5/", include("day5.solution")),
    path("day6/", include("day6.solution")),
    path("day7/", include("day7.solution"))
]
