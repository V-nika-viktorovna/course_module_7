from django import template

register = template.Library()


@register.filter()
def media_filter(data):
    """Шаблонный фильтр. Добавляет к пути папку media."""

    if data:
        return f"/media/{data}"

    return "#"
