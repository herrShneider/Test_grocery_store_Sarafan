from rest_framework import serializers

from config import (AMOUNT_MAX_VALUE, AMOUNT_MIN_VALUE,
                    DECIMALFIELD_DECIMAL_PLACES, DECIMALFIELD_MAX_DIGITS)
from groceries.models import Category, Product, ShoppingCartItem, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = (
            'id',
            'name',
            'slug',
            'image',
        )


class CategorySerializer(serializers.ModelSerializer):

    subcategories = SubcategorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:

        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'image',
            'subcategories',
        )


class ProductSerializer(serializers.ModelSerializer):

    category = serializers.SerializerMethodField()
    subcategory = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )
    images = serializers.SerializerMethodField()

    class Meta:

        model = Product
        fields = (
            'name',
            'slug',
            'category',
            'subcategory',
            'price',
            'images',
        )

    def get_category(self, obj):
        return obj.subcategory.category.slug

    def get_images(self, obj):
        """
        Собирает список изображений продукта в разных размерах.
        """
        images = []
        self._add_image_if_exists(obj.image_small, 'small', images)
        self._add_image_if_exists(obj.image_medium, 'medium', images)
        self._add_image_if_exists(obj.image_large, 'large', images)
        return images

    def _add_image_if_exists(self, image, size_name, images):
        """
        Добавляет изображение в список, если оно существует.
        """
        if image:
            images.append({
                'size': size_name,
                'url': image.url
            })


class ShoppingCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCartItem
        fields = (
            'user',
            'product',
            'amount',
        )

    def validate_amount(self, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                'Количество должно быть числом.'
            )

        if value < AMOUNT_MIN_VALUE:
            raise serializers.ValidationError(
                f'Значение должно быть больше {AMOUNT_MIN_VALUE}'
            )
        if value > AMOUNT_MAX_VALUE:
            raise serializers.ValidationError(
                f'Значение должно быть меньше {AMOUNT_MAX_VALUE}'
            )
        return value


class ShoppingCartReadSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=DECIMALFIELD_MAX_DIGITS,
        decimal_places=DECIMALFIELD_DECIMAL_PLACES,
        read_only=True
    )
    total_product_cost = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartItem
        fields = (
            'product_name',
            'product_price',
            'amount',
            'total_product_cost'
        )

    def get_total_product_cost(self, obj):
        """
        Добавляет стоимость выбранного колличества продукта.
        """
        return obj.product.price * obj.amount
