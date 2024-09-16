from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from groceries.models import Category, Product, Subcategory

admin.site.unregister(Group)

admin.site.empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'show_image',

    )

    @admin.display(description='Картинка')
    def show_image(self, obj):
        return mark_safe(
            f'<img src={obj.image.url} width="80" height="60">'
        )


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'slug',
        'show_image',

    )
    list_filter = (
        'category',
    )

    @admin.display(description='Картинка')
    def show_image(self, obj):
        return mark_safe(
            f'<img src={obj.image.url} width="80" height="60">'
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subcategory',
        'category',
        'slug',
        'show_image',
        'price',

    )
    list_filter = (
        'subcategory__category',
        'subcategory',
    )

    @admin.display(description='Картинка')
    def show_image(self, obj):
        return mark_safe(
            f'<img src={obj.image_original.url} width="80" height="60">'
        )

    @admin.display(description='Категория')
    def category(self, obj):
        return obj.subcategory.category
