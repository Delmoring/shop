# Generated by Django 3.2.9 on 2022-01-28 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('good', '0005_remove_selling_in_carts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selling',
            name='count_goods',
            field=models.IntegerField(default=False),
        ),
    ]