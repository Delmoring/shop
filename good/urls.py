from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', test_out, name = 'test')
]