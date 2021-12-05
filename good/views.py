from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from good.models import Good


def test_out(request):
   # phone = Good.objects.all()


    return render(request, 'good/shop.html')