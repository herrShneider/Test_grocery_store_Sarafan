# Generated by Django 3.2.16 on 2024-09-15 20:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groceries', '0002_auto_20240915_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcartitem',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Значение должно быть больше 1'), django.core.validators.MaxValueValidator(32767, message='Значение должно быть меньше 32767')], verbose_name='Количество'),
            preserve_default=False,
        ),
    ]
