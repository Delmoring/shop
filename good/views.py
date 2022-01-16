from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

#from .forms import *
from .models import *
#from .utils import *


good = Good.objects.all()
cats = Category.objects.all()
def test_out(request):

    return render(request, 'good/index.html', {'good': good, 'cats': cats})

def show_good(request, good_slug):
    show_device = get_object_or_404(Good, slug=good_slug)
    return render(request, 'good/show_device.html', {'show_device': show_device})

def show_category(request, cat_slug):
    c = Category.objects.get(slug=cat_slug)
    good = Good.objects.filter(cat_id = c.pk)

    context = {
        'cats': cats,
        'good': good,
        }


    if len(good) == 0:
        raise Http404()

    return render(request, 'good/index.html', context=context)


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'good/register.html'
    success_url = reverse_lazy('login')

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'good/login.html'

    def get_success_url(self):
        return reverse_lazy('test')

def logout_user(request):
    logout(request)
    return redirect('login')