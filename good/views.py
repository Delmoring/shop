from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.db.models import F
from django.forms.models import model_to_dict
from .models import Goods, Selling
from .utils import SumOrderMixin


class HomeGood(SumOrderMixin, ListView):
    model = Goods
    template_name = 'good/index.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        else:
            return super(HomeGood, self).get(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))


class ShowGood(SumOrderMixin, DetailView):
    model = Goods
    template_name = 'good/show_device.html'
    slug_url_kwarg = 'good_slug'
    context_object_name = 'show_device'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))


class GoodCategory(SumOrderMixin, ListView):
    model = Goods
    template_name = 'good/index.html'
    context_object_name = 'goods'

    def get_queryset(self):
        return Goods.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))


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


class ShowCart(SumOrderMixin, ListView):
    model = Goods
    template_name = 'good/cart.html'
    context_object_name = 'devices_in_cart'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))


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
