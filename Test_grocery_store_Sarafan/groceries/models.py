from django.db import models

from config import (DECIMALFIELD_DECIMAL_PLACES, DECIMALFIELD_MAX_DIGITS,
                    NAME_MAX_LENGTH, SLICE_STR_METHOD_LIMIT, SLUG_MAX_LENGTH)
from groceries.validators import validate_image_exists


class CategorySubcategoryProductBase(models.Model):
    """
    Базовая модель для представлений категорий, подкатегорий и продуктов.
    """

    name = models.CharField(
        verbose_name='Название',
        max_length=NAME_MAX_LENGTH,
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        max_length=SLUG_MAX_LENGTH,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:SLICE_STR_METHOD_LIMIT]


class Category(CategorySubcategoryProductBase):
    """
    Модель для представления категорий продуктов.
    """

    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='categories/images/',
        default=None,
        validators=(validate_image_exists,)
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Subcategory(CategorySubcategoryProductBase):
    """
    Модель для представления подкатегорий продуктов.
    """

    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='subcategories/images/',
        default=None,
        validators=(validate_image_exists,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('name',)


class Product(Category):
    """
    Модель для представления продуктов.
    """

    image_small = models.ImageField(
        verbose_name='Изображение (маленькое)',
        upload_to='products/images/small/',
        default=None,
        validators=(validate_image_exists,)
    )
    image_medium = models.ImageField(
        verbose_name='Изображение (среднее)',
        upload_to='products/images/medium/',
        default=None,
        validators=(validate_image_exists,)
    )
    image_large = models.ImageField(
        verbose_name='Изображение (большое)',
        upload_to='products/images/large/',
        default=None,
        validators=(validate_image_exists,)
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=DECIMALFIELD_MAX_DIGITS,
        decimal_places=DECIMALFIELD_DECIMAL_PLACES,
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        verbose_name='Подкатегория',
    )

    class Meta(Category.Meta):
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)
