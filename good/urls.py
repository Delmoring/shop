from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, re_path

from .views import *

urlpatterns = [
                  path('', test_out, name='test'),
                  path('test/', test2, name='test2')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
