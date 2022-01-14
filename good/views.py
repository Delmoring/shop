from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from good.models import Good



def test_out(request):
    good = Good.objects.all()
    return render(request, 'good/shop.html', {'good': good, 'test_url': test2})

def test2(request):
    good = Good.objects.get(pk=1)
    return render(request, 'good/test.html', [{'good': good}, {'test_url': test2}])