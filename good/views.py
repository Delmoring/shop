from django.contrib.auth.models import User

from django.contrib.auth import logout, login

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, request
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.db.models import F
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SellingForm
from .models import Goods, Category, Selling
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


class ShowGood(SumOrderMixin, DetailView):
    model = Goods
    template_name = 'good/show_device.html'
    slug_url_kwarg = 'good_slug'
    context_object_name = 'show_device'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))


# def show_good(request, good_slug):
#     show_device = get_object_or_404(Goods, slug=good_slug)
#
#     count_goods = list(map(model_to_dict, Selling.objects.filter(User_id=request.user)))
#     devices_in_cart = list(map(model_to_dict, Goods.objects.filter(carts=request.user)))
#     for device in range(len(devices_in_cart)):
#         devices_in_cart[device]['count'] = count_goods[device]['count_goods']
#         devices_in_cart[device]['total_price'] = devices_in_cart[device]['price'] * count_goods[device]['count_goods']
#
#     sum_order = 0
#     for device in devices_in_cart:
#         sum_order += device['total_price']
#
#     return render(request, 'good/show_device.html', {'show_device': show_device, 'sum_order': sum_order})

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


# def show_category(request, cat_slug):
#     c = Category.objects.get(slug=cat_slug)
#     goods = Goods.objects.filter(cat_id=c.pk)
#
#     paginator = Paginator(goods, 2)
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     count_goods = list(map(model_to_dict, Selling.objects.filter(User_id=request.user)))
#     devices_in_cart = list(map(model_to_dict, Goods.objects.filter(carts=request.user)))
#     for device in range(len(devices_in_cart)):
#         devices_in_cart[device]['count'] = count_goods[device]['count_goods']
#         devices_in_cart[device]['total_price'] = devices_in_cart[device]['price'] * count_goods[device]['count_goods']
#
#     sum_order = 0
#     for device in devices_in_cart:
#         sum_order += device['total_price']
#
#     context = {
#         'page_obj': page_obj,
#         'cats': cats,
#         'good': goods,
#         'count': goods.count(),
#         'sum_order': sum_order,
#
#     }
#
#     if len(goods) == 0:
#         raise Http404()
#
#     return render(request, 'good/index.html', context=context)


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


# def show_cart(request):
#     count_goods = list(map(model_to_dict, Selling.objects.filter(User_id=request.user)))
#     devices_in_cart = list(map(model_to_dict, Goods.objects.filter(carts=request.user)))
#     for device in range(len(devices_in_cart)):
#         devices_in_cart[device]['count'] = count_goods[device]['count_goods']
#         devices_in_cart[device]['total_price'] = devices_in_cart[device]['price'] * count_goods[device]['count_goods']
#
#     sum_order = 0
#     for device in devices_in_cart:
#         sum_order += device['total_price']
#
#     return render(request, 'good/cart.html',
#                   {'devices_in_cart': devices_in_cart, 'sum_order': sum_order, 'count_goods': count_goods})

class AddCart(SumOrderMixin, CreateView):
    form_class = SellingForm
    slug_url_kwarg = 'good_slug'
    template_name = 'good/add_cart.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        f = SellingForm(self.request.POST)
        if f.is_valid():
            new_author = f.save()
            new_author.count_goods = Selling.objects.filter(User_id=request.user).update(count_goods=F('count_goods'))
            new_author.save()
            f.save_m2m()

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        return dict(list(context.items()) + list(c_def.items()))




#         good_slug = self.kwargs.get('good_slug', None)
#         device = get_object_or_404(Goods, slug=good_slug)
#         u = User.objects.get(username=self.request.user)
#         return device.carts.add(u)

# class AddCart(SumOrderMixin, DetailView):
#     model = Goods
#     template_name = 'good/show_device.html'
#
#     context_object_name = 'device'
#
#     def get(self, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return redirect('login')
#         else:
#             return redirect('cart')
#
#     def get_queryset(self, **kwargs):
#         good_slug = self.kwargs.get('good_slug', None)
#         device = get_object_or_404(Goods, slug=good_slug)
#         u = User.objects.get(username=self.request.user)
#         return device.carts.add(u)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['good_slug'] = self.kwargs['good_slug']
#         c_def = self.get_user_context(**kwargs)
#         return dict(list(context.items()) + list(c_def.items()))


# def add_cart(request, good_slug):
#
#     if request.user.is_authenticated:
#         device = get_object_or_404(Goods, slug=good_slug)
#         u = User.objects.get(username=request.user)
#         device.carts.add(u)
#
        # Selling.objects.get_or_create(User_id=request.user, Goods_id=device.pk)
        # Selling.objects.filter(User_id=request.user, Goods_id=device.pk).update(count_goods=F('count_goods') + 1)
#
#         count_goods = list(map(model_to_dict, Selling.objects.filter(User_id=request.user)))
#         devices_in_cart = list(map(model_to_dict, Goods.objects.filter(carts=request.user)))
#         for device in range(len(devices_in_cart)):
#             devices_in_cart[device]['count'] = count_goods[device]['count_goods']
#             devices_in_cart[device]['total_price'] = devices_in_cart[device]['price'] * count_goods[device][
#                 'count_goods']
#
#         sum_order = 0
#         for device in devices_in_cart:
#             sum_order += device['total_price']
#
#         return render(request, 'good/show_device.html', {'show_device': device, 'sum_order': sum_order})
#     return HttpResponse("Для добавления товара в корзину необходимо быть авторизованным пользователем")


def nothing(request):
    return HttpResponse("Пока нет ничего")
