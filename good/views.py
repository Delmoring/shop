from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def test_out(request):
    return HttpResponse('Тестовый вывод')