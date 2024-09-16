from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image

from config import (AMOUNT_MAX_VALUE, AMOUNT_MIN_VALUE,
                    DECIMALFIELD_DECIMAL_PLACES, DECIMALFIELD_MAX_DIGITS,
                    IMAGE_SIZES, NAME_MAX_LENGTH, SLICE_STR_METHOD_LIMIT,
                    SLUG_MAX_LENGTH)
from groceries.validators import validate_image_exists

User = get_user_model()


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
        related_name='subcategories',
    )

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('name',)


class Product(CategorySubcategoryProductBase):
    """
    Модель для представления продуктов.
    """

    image_original = models.ImageField(
        verbose_name='Оригинальное изображение',
        upload_to='products/images/original/',
        validators=(validate_image_exists,)
    )
    image_small = models.ImageField(
        verbose_name='Изображение (маленькое)',
        upload_to='products/images/small/',
        null=True,
        blank=True
    )
    image_medium = models.ImageField(
        verbose_name='Изображение (среднее)',
        upload_to='products/images/medium/',
        null=True,
        blank=True
    )
    image_large = models.ImageField(
        verbose_name='Изображение (большое)',
        upload_to='products/images/large/',
        null=True,
        blank=True
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
        related_name='products',
    )

    class Meta(Category.Meta):
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения для изменения размеров изображения.
        """
        super().save(*args, **kwargs)

        if self.image_original:
            for size_name, (width, height) in IMAGE_SIZES.items():
                self._resize_image(
                    self.image_original,
                    width,
                    height,
                    size_name
                )

    def _resize_image(self, image, width, height, size_name):
        """
        Метод для изменения размера изображения.
        """
        img = Image.open(image)
        img = img.resize((width, height), Image.Resampling.LANCZOS)

        # Создаем буфер для сохранения нового изображения
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG')

        # Генерируем название файла
        new_image = ContentFile(thumb_io.getvalue(), name=image.name)

        # Сохраняем изображение в нужное поле
        if size_name == 'small':
            self.image_small.save(new_image.name, new_image, save=False)
        elif size_name == 'medium':
            self.image_medium.save(new_image.name, new_image, save=False)
        elif size_name == 'large':
            self.image_large.save(new_image.name, new_image, save=False)

        # Сохраняем объект после изменения изображения
        super().save(update_fields=[f'image_{size_name}'])


class ShoppingCartItem(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Продукт',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(
                AMOUNT_MIN_VALUE,
                message=f'Значение должно быть больше {AMOUNT_MIN_VALUE}'
            ),
            MaxValueValidator(
                AMOUNT_MAX_VALUE,
                message=f'Значение должно быть меньше {AMOUNT_MAX_VALUE}'
            ),
        )
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shoppingcart_items'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'product'),
                name='user_product_unique_constraint',
            ),
        )

    def __str__(self):
        return f'Корзина {self.user} - Продукт: {self.product}'
