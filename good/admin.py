from django.contrib import admin

from .models import *

class GoodAdmin(admin.ModelAdmin):
    list_display = ('id',  'cat_name', 'model', 'specifications', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'model')
    search_fields = (['cat_name'])
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("model",)}


admin.site.register(Good, GoodAdmin)
