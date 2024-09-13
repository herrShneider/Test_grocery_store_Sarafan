from django.core.exceptions import ValidationError


def validate_image_exists(image):
    if not image:
        raise ValidationError(
            'Создание рецепта без картинки - невозможно.'
        )
    return image
