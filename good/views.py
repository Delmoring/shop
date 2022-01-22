from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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

# from .forms import *
from .models import *

# from .utils import *


goods = Goods.objects.all()
cats = Category.objects.all()


def index(request):
    # good_list = Good.objects.all()
    paginator = Paginator(goods, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'good/index.html', {'page_obj': page_obj, 'cats': cats, 'count': goods.count()})


def show_good(request, good_slug):
    show_device = get_object_or_404(Goods, slug=good_slug)
    return render(request, 'good/show_device.html', {'show_device': show_device})


def show_category(request, cat_slug):
    c = Category.objects.get(slug=cat_slug)
    goods = Goods.objects.filter(cat_id=c.pk)

    paginator = Paginator(goods, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'cats': cats,
        'good': goods,
        'count': goods.count()
    }

    if len(goods) == 0:
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
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')


def show_cart(request):
    if request.user.is_authenticated:
        u = User.objects.get(username=request.user)
        return HttpResponse(f"id текущего пользователя = id {u.pk}")
    return HttpResponse("Для добавления товара в корзину необходимо быть авторизированным пользователем")


def add_cart(request, good_slug):
    device = get_object_or_404(Goods, slug=good_slug)
    return render(request, 'good/show_device.html', {'show_device': show_device})



def nothing(request):
    return HttpResponse("Пока нет ничего")
