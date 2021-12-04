from django.db import models
from django.urls import reverse

class Good(models.Model):
    cat_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    model = models.CharField(max_length=255)
    specifications = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.cat_name

    class Category(models.Model):
        name = models.CharField(max_length=100, db_index=True)
        slug = models.SlugField(max_length=255, unique=True, db_index=True)

        def __str__(self):
            return self.name