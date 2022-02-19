from django.contrib.auth.models import User

from django.contrib.auth import logout, login

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.db.models import F
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Goods, Category, Selling
from .utils import SumOrderMixin


class HomeGood(SumOrderMixin, ListView):
    model = Goods
    template_name = 'good/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))


# def index(request):
#     if request.user.is_authenticated:
#         paginator = Paginator(goods, 2)
#
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#
#
#
#         return render(request, 'good/index.html',
#                   {'page_obj': page_obj, 'cats': cats, 'count': goods.count(), 'sum_order': sum_order})
#     else:
#         return redirect('login')


def show_good(request, good_slug):
    show_device = get_object_or_404(Goods, slug=good_slug)

    count_goods = list(map(model_to_dict, Selling.objects.filter(User_id=request.user)))
    devices_in_cart = list(map(model_to_dict, Goods.objects.filter(carts=request.user)))
    for device in range(len(devices_in_cart)):
        devices_in_cart[device]['count'] = count_goods[device]['count_goods']
        devices_in_cart[device]['total_price'] = devices_in_cart[device]['price'] * count_goods[device]['count_goods']

    sum_order = 0
    for device in devices_in_cart:
        sum_order += device['total_price']

    return render(request, 'good/show_device.html', {'show_device': show_device, 'sum_order': sum_order})


def show_category(request, cat_slug):
    c = Category.objects.get(slug=cat_slug)
    goods = Goods.objects.filter(cat_id=c.pk)

    paginator = Paginator(goods, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    count_goods = list(map(model_to_dict, Selling.objects.filter(User_id=request.user)))
    devices_in_cart = list(map(model_to_dict, Goods.objects.filter(carts=request.user)))
    for device in range(len(devices_in_cart)):
        devices_in_cart[device]['count'] = count_goods[device]['count_goods']
        devices_in_cart[device]['total_price'] = devices_in_cart[device]['price'] * count_goods[device]['count_goods']

    sum_order = 0
    for device in devices_in_cart:
        sum_order += device['total_price']

    context = {
        'page_obj': page_obj,
        'cats': cats,
        'good': goods,
        'count': goods.count(),
        'sum_order': sum_order,

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
    count_goods = list(map(model_to_dict, Selling.objects.filter(User_id=request.user)))
    devices_in_cart = list(map(model_to_dict, Goods.objects.filter(carts=request.user)))
    for device in range(len(devices_in_cart)):
        devices_in_cart[device]['count'] = count_goods[device]['count_goods']
        devices_in_cart[device]['total_price'] = devices_in_cart[device]['price'] * count_goods[device]['count_goods']

    sum_order = 0
    for device in devices_in_cart:
        sum_order += device['total_price']

    return render(request, 'good/cart.html',
                  {'devices_in_cart': devices_in_cart, 'sum_order': sum_order, 'count_goods': count_goods})


def add_cart(request, good_slug):
    if request.user.is_authenticated:
        device = get_object_or_404(Goods, slug=good_slug)
        u = User.objects.get(username=request.user)
        device.carts.add(u)

        Selling.objects.get_or_create(User_id=request.user, Goods_id=device.pk)
        Selling.objects.filter(User_id=request.user, Goods_id=device.pk).update(count_goods=F('count_goods') + 1)

        count_goods = list(map(model_to_dict, Selling.objects.filter(User_id=request.user)))
        devices_in_cart = list(map(model_to_dict, Goods.objects.filter(carts=request.user)))
        for device in range(len(devices_in_cart)):
            devices_in_cart[device]['count'] = count_goods[device]['count_goods']
            devices_in_cart[device]['total_price'] = devices_in_cart[device]['price'] * count_goods[device][
                'count_goods']

        sum_order = 0
        for device in devices_in_cart:
            sum_order += device['total_price']

        return render(request, 'good/show_device.html', {'show_device': device, 'sum_order': sum_order})
    return HttpResponse("Для добавления товара в корзину необходимо быть авторизованным пользователем")


def nothing(request):
    return HttpResponse("Пока нет ничего")
