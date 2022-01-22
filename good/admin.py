from django.contrib import admin

from .models import *


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'model')
    # search_fields = (['cat_name'])
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("model",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Goods, GoodsAdmin)
admin.site.register(Category, CategoryAdmin)
