from django.db.models import QuerySet


def generate_shopping_list_text(ingredients: QuerySet) -> str:
    """Формировать текстовое содержимое для файла списка покупок."""
    lines = ['Список покупок:', '']

    for ing in ingredients:
        name = ing['ingredient__name']
        unit = ing['ingredient__measurement_unit']
        amount = ing['amount']
        lines.append(f'{name} ({unit}) — {amount}')

    return '\n'.join(lines) + '\n'
