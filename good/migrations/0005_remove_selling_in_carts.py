# Generated by Django 3.2.9 on 2022-01-28 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('good', '0004_selling_count_goods'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selling',
            name='in_carts',
        ),
    ]
