from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Good(models.Model):
    cat_name = models.CharField(max_length=255, verbose_name="Название устройства" )
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    model = models.CharField(max_length=255, verbose_name="Модель")
    specifications = models.TextField(blank=True, verbose_name="Технические характеристики")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    photo2 = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Дополнительное фото(2)")
    photo3 = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Дополнительное фото(3)")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    price = models.IntegerField(default=True, verbose_name="Цена")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    carts = models.ManyToManyField(User)

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse('show_good', kwargs={'good_slug': self.slug})

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_category', kwargs={'cat_slug': self.slug})