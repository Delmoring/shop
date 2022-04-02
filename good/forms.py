
from django.forms import ModelForm


from .models import Selling


class SellingForm(ModelForm):
    class Meta:
        model = Selling
        fields = ['Goods', 'User', 'count_goods']




