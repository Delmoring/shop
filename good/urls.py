from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path

from .views import *

urlpatterns = [
                  path('', test_out, name='test'),
                  path('show_good/<slug:good_slug>/', show_good, name='show_good'),
                  path('show_category/<int:cat_id>', show_category, name='show_category'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
