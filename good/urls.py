from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path

from .views import *

urlpatterns = [
                  path('', index, name='index'),
                  path('show_good/<slug:good_slug>/', show_good, name='show_good'),
                  path('show_category/<slug:cat_slug>', show_category, name='show_category'),
                  path('register', RegisterUser.as_view(), name='register'),
                  path('login', LoginUser.as_view(), name='login'),
                  path('logout', logout_user, name='logout'),
                  path('empty_page', nothing, name='empty_page'),
                  path('cart/', show_cart, name='cart'),
                  path('add_cart/<slug:good_slug>', add_cart, name='add_cart'),
                  path('del_cart/', delete, name='del_cart')



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
