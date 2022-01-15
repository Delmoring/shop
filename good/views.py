from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from good.models import Good


good = Good.objects.all()
def test_out(request):

    return render(request, 'good/shop.html', {'good': good})

def test2(request):
    return render(request, 'good/show_device.html')