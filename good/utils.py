from django.shortcuts import redirect
from django.views.generic import ListView

from .models import *
from django.forms.models import model_to_dict




class SumOrderMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        goods = Goods.objects.all()
        cats = Category.objects.all()
        data = kwargs

        count_goods = list(map(model_to_dict, Selling.objects.filter(User_id=self.request.user)))
        devices_in_cart = list(map(model_to_dict, Goods.objects.filter(carts=self.request.user)))
        for device in range(len(devices_in_cart)):
            devices_in_cart[device]['count'] = count_goods[device]['count_goods']
            devices_in_cart[device]['total_price'] = devices_in_cart[device]['price'] * count_goods[device][
                'count_goods']

        sum_order = 0
        for device in devices_in_cart:
            sum_order += device['total_price']

        data['sum_order'] = sum_order
        data['cats'] = cats
        data['count'] = goods.count()

        return data



