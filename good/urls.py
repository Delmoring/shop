from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
                  path('', HomeGood.as_view(), name='index'),
                  path('show_good/<slug:good_slug>/', ShowGood.as_view(), name='show_good'),
                  path('show_category/<slug:cat_slug>', GoodCategory.as_view(), name='show_category'),
                  path('register/', RegisterUser.as_view(), name='register'),
                  path('login/', LoginUser.as_view(), name='login'),
                  path('logout/', logout_user, name='logout'),
                  path('empty_page/', nothing, name='empty_page'),
                  path('cart/', ShowCart.as_view(), name='cart'),
                  path('add_cart/<slug:good_slug>', add_cart, name='add_cart'),






              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
