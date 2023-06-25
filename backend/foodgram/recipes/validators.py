import re

from django.core.exceptions import ValidationError


def validate_hex_color(value):
    pattern = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
    if not pattern.match(value):
        raise ValidationError(
            "Значение поля 'Цвет' должно быть допустимым hex-цветом"
        )
