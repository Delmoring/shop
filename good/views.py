from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
# Create your views here.
from good.models import Good


good = Good.objects.all()
def test_out(request):

    return render(request, 'good/index.html', {'good': good})

def show_good(request, good_slug):
    show_device = get_object_or_404(Good, slug=good_slug)
    return render(request, 'good/show_device.html', {'show_device': show_device})

