from rest_framework import serializers

from recipes.models import Ingredient


def validate_ingredients_data(ingredients):
    """Валидация списка ингредиентов для сериализатора рецептов."""
    if ingredients is None:
        raise serializers.ValidationError(
            {'ingredients': 'Это поле обязательно.'}
        )
    if not ingredients:
        raise serializers.ValidationError(
            {'ingredients': 'Нужен хотя бы один ингредиент.'}
        )

    ingredients_list = []
    for item in ingredients:
        if "id" not in item:
            raise serializers.ValidationError(
                {'ingredients': 'У ингредиента должен быть id.'}
            )

        ingredient_id = item['id']
        if not Ingredient.objects.filter(id=ingredient_id).exists():
            raise serializers.ValidationError(
                {
                    'ingredients': (
                        f'Ингредиент {ingredient_id} не существует.'
                    )
                }
            )

        if ingredient_id in ingredients_list:
            raise serializers.ValidationError(
                {'ingredients': 'Ингредиенты не должны повторяться.'}
            )
        ingredients_list.append(ingredient_id)
    return ingredients


def validate_tags_data(tags):
    """Валидация списка тегов для сериализатора рецептов."""
    if tags is None:
        raise serializers.ValidationError({'tags': 'Это поле обязательно.'})
    if not tags:
        raise serializers.ValidationError({'tags': 'Нужен хотя бы один тег.'})

    tags_list = []
    for tag_id in tags:
        if tag_id in tags_list:
            raise serializers.ValidationError(
                {'tags': 'Теги не должны повторяться.'}
            )
        tags_list.append(tag_id)
    return tags
