# Generated by Django 3.2.9 on 2022-01-26 16:25

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('good', '0002_auto_20220122_1749'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='isSaled',
            new_name='Selling',
        ),
    ]
