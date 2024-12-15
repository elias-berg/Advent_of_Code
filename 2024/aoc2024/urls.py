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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
import os
import re

# Just use Regex to tell what days are ready to be served
dirs = os.listdir(settings.BASE_DIR)
days = list(filter(lambda dir: not re.match("^day\d*", dir) == None, dirs))
urlpatterns = list(map(lambda day: path(f"{day}/", include(f"{day}.solution")), days))

# urlpatterns.append(
#   path('admin/', admin.site.urls),
# )
